#!/usr/bin/env python3.8

from sidchip import SIDChip
from sidchip.effect import Vibrato
import time
from math import sin


class SoundSID:

    def __init__(self):
        # common sid chip for all instances (cant play more than 1 instance at a time)
        import pysid
        self.pysid = pysid

        self.sid = SIDChip()
        self.sid.filter.volume = 10

        #standup setup
        self.setup_voices()
        self.setup_tempo()
        self.setup_music()


    def update_sid_chip(self):
        regs = self.sid.get_regs()
        for x in range(25):
            self.pysid.write_reg(x, regs[x])


    def setup_voices(self):

        self.sid.voice1 = Vibrato(self.sid.voice1, frequency=10, depth=100)
        self.sid.voice1.midi_to_frequency(69)


        self.sid.filter.voice2 = True
        self.sid.filter.low_pass = True

        for voice in self.sid.voices:
            voice.pulse = False
            voice.sawtooth = False
            voice.noise = False
            voice.triangle = False
            voice.gate = True
            voice.duty_cycle = voice.max_duty_cycle / 2 # 50% duty cycle is a square wave, bro!

        self.sid.voice1.sawtooth = True
        self.sid.voice2.pulse = True
        self.sid.voice3.noise = True

        self.sid.voice1.adsr(0, 0, 13, 0)
        self.sid.voice2.adsr(10, 5, 3, 10)
        self.sid.voice3.adsr(0, 0, 13, 6)

    def setup_tempo(self):

        self.vibrato_depth = 100
        self.vibrato_speed = 40

        self.filter_speed = 1

        self.note_speed = 4


    def setup_music(self):

        self.notes = [
                60, 60, 60, 60, 60, 60, 60, 60,
                62, 62, 62, 62, 62, 62, 62, 62,
                64, 64, 64, 64, 64, 64, 64, 64,
                67, 67, 67, 67, 67, 67, 67, 67,

                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,
                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,


                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,
                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,

                ]

        self.base_notes = [
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,

                31, 31, 31, 31, 32, 32, 32, 32,
                34, 34, 34, 34, 35, 35, 35, 35,
                31, 31, 31, 31, 32, 32, 32, 32,
                35, 35, 35, 35, 34, 34, 34, 34,

                31+12, 31, 31+12, 31, 32+12, 32, 32+12, 32,
                34+12, 34, 34+12, 34, 35+12, 35, 35+12, 35,
                31+12, 31, 31+12, 31, 32+12, 32, 32+12, 32,
                35+12, 35, 35+12, 35, 34+12, 34, 34+12, 34]

        self.drum_notes = [
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                90,90,90,90,90,90,90,90,
                90,90,60,90,90,90,60,90,

                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 20, 60, 90, 20, 90, 60, 60,

                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 20, 60, 90, 20, 90, 60, 60]



    def start_play(self):

        self.start = None
        self.last_note = 0



    def play_note(self):

        if self.start is None:
            self.start = time.time()

        now = time.time()
        note_index = (now - self.start) * self.note_speed


        b = int(note_index % len(self.base_notes))
        n = int(note_index % len(self.notes))
        dr = int(note_index % len(self.drum_notes))

        time_in_drum = note_index % len(self.drum_notes) - dr


        self.sid.voice1.midi_to_frequency(self.base_notes[b])
        self.sid.voice2.midi_to_frequency(self.notes[n])
        self.sid.voice3.midi_to_frequency(self.drum_notes[dr])

        print(f"b = {b},  base_notes[b] = {self.base_notes[b]}")

        c = ((sin(now * self.filter_speed) + 1)/2)
        self.sid.filter.cutoff = (self.sid.filter.max_cutoff / 4) + (c * (self.sid.filter.max_cutoff / 2))
        self.sid.filter.resonance = (1.0 - c) * self.sid.filter.max_resonance

        d = ((sin(now * self.vibrato_speed) + 1)/2)
        self.sid.voice2.frequency += d * self.vibrato_depth

        self.sid.voice1.gate = self.base_notes[b] > 0
        self.sid.voice3.gate = self.drum_notes[dr] > 0 and time_in_drum < 0.3

        if self.notes[n] != self.last_note:
            self.sid.voice2.gate = False
            self.update_sid_chip()
            self.last_note = self.notes[n]

        self.sid.voice2.gate = True

        self.update_sid_chip()








##################################################################
#base
class Instrument1:
    def configure(self, voice):
        self.hit_note = False
        self.duration = None

        self.vibrato_depth = 100
        self.vibrato_speed = 40

     #   voice.sawtooth = True
        voice.adsr(0, 0, 13, 0)
#n
class Instrument2:
    def configure(self, voice):
        self.hit_note = True
        self.duration = None
        voice.pulse = True
        voice.adsr(10, 5, 3, 10)


#drums
class Instrument3:
    def configure(self, voice):
        self.hit_note = False
        self.duration = 0.3
      #  voice.noise = True
        voice.adsr(0, 0, 13, 6)


class Sound:
    def __init__(self, instrument, note, start):
        self.instrument = instrument
        self.note = note
        self.start = start

    def __str__(self):
        return f"Sound(note={self.note})"

    def set_frequency(self, voice, now):
        voice.sid_voice.midi_to_frequency(self.note)



class Voice:

    def __init__(self, sid_voice):

        self.sid_voice = sid_voice
        self.instrument = None

        self.music_start = None
        self.note_speed = None
        self.notes = None


        self.sound = None
        self.last_sound = None

        self.last_n = -1


    def set_sound(self, sound):
        print(f"sound = {sound}")
        self.sound = sound

    def peek_sound(self):

        self.play_note()

        is_new_sound = True
        if self.last_sound is not None and self.sound.note == self.last_sound.note:
            is_new_sound = False

        return (self.sound, is_new_sound)

    def get_sound(self):

        self.play_note()

        is_new_sound = True
        if self.last_sound is not None and self.sound.note == self.last_sound.note:
            is_new_sound = False
        self.last_sound = self.sound

        return (self.sound, is_new_sound)




    def play_note(self):

        if self.notes:

            now = time.time()
            if self.music_start is None:
                self.music_start = now

            note_index = (now - self.music_start) * self.note_speed
            n = int(note_index % len(self.notes))
            note = self.notes[n]
            time_in = note_index % len(self.notes) - n

            if n != self.last_n:
                self.set_sound(Sound(self.instrument, note, now))
                self.last_n = n
                print(n)


notes = [
                60, 60, 60, 60, 60, 60, 60, 60,
                62, 62, 62, 62, 62, 62, 62, 62,
                64, 64, 64, 64, 64, 64, 64, 64,
                67, 67, 67, 67, 67, 67, 67, 67,

                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,
                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,

                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,
                60, 60, 62, 64, 65, 67, 67, 65,
                60, 60, 62, 64, 65, 67, 71, 68,

                ]

base_notes = [
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,

                31, 31, 31, 31, 32, 32, 32, 32,
                34, 34, 34, 34, 35, 35, 35, 35,
                31, 31, 31, 31, 32, 32, 32, 32,
                35, 35, 35, 35, 34, 34, 34, 34,

                31+12, 31, 31+12, 31, 32+12, 32, 32+12, 32,
                34+12, 34, 34+12, 34, 35+12, 35, 35+12, 35,
                31+12, 31, 31+12, 31, 32+12, 32, 32+12, 32,
                35+12, 35, 35+12, 35, 34+12, 34, 34+12, 34]

drum_notes = [
                0,0,0,0,0,0,0,0,
                0,0,0,0,0,0,0,0,
                90,90,90,90,90,90,90,90,
                90,90,60,90,90,90,60,90,

                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 20, 60, 90, 20, 90, 60, 60,

                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 90, 60, 90, 20, 90, 60, 90,
                20, 20, 60, 90, 20, 90, 60, 60]




class SoundManager:


    def __init__(self):
        # common sid chip for all instances (cant play more than 1 instance at a time)
        import pysid
        self.pysid = pysid

        self.sid = SIDChip()

        self.setup_voices()

        self.sid.voice1 = Vibrato(self.sid.voice1, frequency=10, depth=100)

        self.voices = [Voice(self.sid.voice1), Voice(self.sid.voice2), Voice(self.sid.voice3)]

    def setup_voices(self):

        for voice in self.sid.voices:
            voice.pulse = False
            voice.sawtooth = False
            voice.noise = False
            voice.triangle = False
            voice.gate = True
            voice.duty_cycle = voice.max_duty_cycle / 2 # 50% duty cycle is a square wave, bro!



    def update_sid_chip(self):
        regs = self.sid.get_regs()
        for x in range(25):
            self.pysid.write_reg(x, regs[x])


    def set_filter(self):
        self.sid.filter.volume = 10
        self.sid.filter.voice2 = True
        self.sid.filter.low_pass = True
        self.filter_speed = 1


    def set_voice(self, n, instrument):
        self.voices[n-1].instrument = instrument


    def set_music(self, n, notes, note_speed=4):
        self.voices[n-1].notes = notes
        self.voices[n-1].note_speed = note_speed


    def tick(self):

        now = time.time()

        c = ((sin(now * self.filter_speed) + 1)/2)
        self.sid.filter.cutoff = (self.sid.filter.max_cutoff / 4) + (c * (self.sid.filter.max_cutoff / 2))
        self.sid.filter.resonance = (1.0 - c) * self.sid.filter.max_resonance

        for voice in [self.voices[1]]: # self.voices:

            sound, is_new_sound = voice.peek_sound()


            # configure voice (it might change over time)
            sound.instrument.configure(voice.sid_voice)

            # set frequency of sound
            sound.set_frequency(voice, now)

            # end note?
            voice.sid_voice.gate = sound.note > 0 and (sound.instrument.duration is None or (now - sound.start) < sound.instrument.duration)

            # toggle off to hit note
            if sound.instrument.hit_note and is_new_sound:
                voice.sid_voice.gate = False

        self.update_sid_chip()

        for voice in [self.voices[1]]: # self.voices:
            sound, is_new_sound = voice.get_sound()
            # toggle on to hit note
            voice.sid_voice.gate = sound.note > 0 and (sound.instrument.duration is None or (now - sound.start) < sound.instrument.duration)

        self.update_sid_chip()





def main():

    sm = SoundManager()

    sm.set_voice(1, Instrument1())
    sm.set_voice(2, Instrument2())
    sm.set_voice(3, Instrument3())

    sm.set_music(1, base_notes)
    sm.set_music(2, notes)
    sm.set_music(3, drum_notes)

    sm.set_filter()

    while True:

        time.sleep(0.001)
        sm.tick()


def old_main():

    sid = SoundSID()

    sid.start_play()
    while True:
        time.sleep(0.001)
        sid.play_note()






if __name__=="__main__":
    old_main()
  #  main()

