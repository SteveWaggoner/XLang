#!/usr/bin/env python3.8

from sidchip import SIDChip
import time
from math import sin

class VoiceUtils:

    attack_ms = [2,8,16,24,38,56,68,80,100,250,500,800,1000,3000,5000,8000]
    decay_ms = [6,24,48,72,114,168,204,240,300,750,1500,2400,3000,9000,15000,24000]
    release_ms = [6,24,48,72,114,168,204,240,300,750,1500,2400,3000,9000,15000,24000]

    def get_duration(voice):
        return VoiceUtils.attack_ms[voice.attack] + VoiceUtils.decay_ms[voice.decay] + VoiceUtils.release_ms[voice.release]

    def set_frequency(voice, midi_note, now, effects=[]):
        voice.midi_to_frequency(midi_note)
        for effect in effects:
            voice.frequency = effect.change_frequency(voice.frequency, now)

    def clear_waves(voice):
        voice.noise    = False
        voice.pulse    = False
        voice.triangle = False
        voice.sawtooth = False


class Sound:
    def __init__(self, instrument, is_sfx, extra):
        self.instrument = instrument
        self.is_sfx = is_sfx
        self.extra = extra

        self.start_time = None
        self.voice = None

    def update_voice(self, now):
        return self.instrument.update_voice(self.voice, now, now - self.start_time, self.extra)


class SoundManager:

    def __init__(self):
        # common sid chip for all instances (cant play more than 1 instance at a time)
        import pysid
        self.pysid = pysid
        self.sid = SIDChip()
        self.init_sid()

        self.sounds = [None,None,None]
        self.last_voice_sustain = [0,0,0]


    def init_sid(self):

        for voice in self.sid.voices:
            VoiceUtils.clear_waves(voice)
            voice.gate = True
            voice.duty_cycle = voice.max_duty_cycle / 2 # 50% duty cycle is a square wave, bro!

        self.sid.filter.volume = 10


    def update_sid_chip(self):

        # when increasing sustain must toggle gate (see https://www.lemon64.com/forum/viewtopic.php?t=63107)
        toggle = [False,False,False]
        needs_toggle = False
        for i in range(3):
            if self.last_voice_sustain[i] < self.sid.voices[i].sustain and self.sid.voices[i].gate == True:
                toggle[i] = True
                needs_toggle = True
            self.last_voice_sustain[i] = self.sid.voices[i].sustain

        if needs_toggle:
            for i in range(3):
                if toggle[i]:
                    self.sid.voices[i].gate = False
            self.raw_update_sid_chip()
            for i in range(3):
                if toggle[i]:
                    self.sid.voices[i].gate = True

        self.raw_update_sid_chip()


    def raw_update_sid_chip(self):

        regs = self.sid.get_regs()
        for x in range(25):
            self.pysid.write_reg(x, regs[x])


    def start(self, now, sound, nvoice):

        # find a sid voice to use
        if sound.is_sfx or self.sounds[nvoice] is None or self.sounds[nvoice].is_sfx==False:

            sound.voice = self.sid.voices[nvoice]
            self.sounds[nvoice] = sound

            # save so we can update in tick
            sound.start_time = now

            # start the sound
            sound.voice.gate = True
            sound.update_voice(now)

            self.update_sid_chip()


    def tick(self, now):

        has_active = False
        for n, sound in enumerate(self.sounds):
            if sound is not None:
                has_active = True
                is_active = sound.update_voice(now)
                if not is_active:
                    self.sounds[n] = None

        if has_active:
            self.update_sid_chip()


##################################################################

class VibratoEffect:

    def __init__(self, vibrato_speed, vibrato_depth):
        self.vibrato_speed = vibrato_speed
        self.vibrato_depth = vibrato_depth

    def change_frequency(self, frequency, now):
        # now is millis
        vibrato = ((sin((now/1000) * self.vibrato_speed) + 1)/2) * self.vibrato_depth
        return frequency + vibrato

##################################################################
class Note:
    def __init__(self, midi_note, time_in, track):
        self.midi_note = midi_note
        self.time_in = time_in
        self.track = track

class Track:

    def __init__(self, track_index, instrument, notes):
        self.track_index = track_index
        self.instrument = instrument
        self.notes = notes
        self.last_n = None
        self.start_ms = None

    def get_note(self, now):

        if self.start_ms is None:
            self.start_ms = now

        elapsed_ms = now - self.start_ms

        # note speed = 4 beats a second
        beats_per_second = 4
        note_index = (elapsed_ms / 1000.0) * beats_per_second
        n          = int(note_index % len(self.notes))
        midi_note  = self.notes[n]
        time_in    = note_index % len(self.notes) - n

        if n != self.last_n:
            self.last_n = n
            print(str(n)+ " midi_note = "+str(midi_note)+" "+str(elapsed_ms))
            if midi_note > 0:
                return Note(midi_note, time_in, self)

        return None


class MusicManager:

    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.tracks = [None,None,None]

    def set_track(self, track_index, instrument, notes):
        self.tracks[track_index-1] = Track(track_index, instrument, notes)

    def play_note(self, now, note):
        sound = Sound(note.track.instrument, is_sfx=False, extra=note)
        nvoice = note.track.track_index - 1  #track index == sid voice to use
        self.sound_manager.start(now, sound, nvoice)

    def tick(self, now):
        for track in self.tracks:
            if track:
                note = track.get_note(now)
                if note:
                    self.play_note(now, note)

##################################################################

start = time.time()
def set_filter(sid):

    global start
    sid.filter.volume = 10
    sid.filter.voice2 = True
    sid.filter.low_pass = True

    now = time.time() - start  # rel time
    filter_speed = 1
    c = ((sin(now * filter_speed) + 1)/2)
    sid.filter.cutoff = (sid.filter.max_cutoff / 4) + (c * (sid.filter.max_cutoff / 2))
    sid.filter.resonance = (1.0 - c) * sid.filter.max_resonance

