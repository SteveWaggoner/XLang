#!/usr/bin/env python3.8

from sound import VibratoEffect, VoiceUtils

##################################################################

class SongA:
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


##################################################################
#base

class Instrument1:
    def __init__(self):
        self.effects = [ VibratoEffect(vibrato_speed = 10, vibrato_depth = 100) ]

    def update_voice(self, voice, now, elapsed_ms, extra):
        VoiceUtils.clear_waves(voice)
        voice.sawtooth = True

        voice.attack = 0
        voice.decay = 0
        voice.sustain = 8
        voice.release = 0

        note = extra #passed in note
        VoiceUtils.set_frequency(voice, note.midi_note, now, self.effects)

        is_active = elapsed_ms < 2000
        return is_active



#n
class Instrument2:
    def __init__(self):
        self.effects = [ VibratoEffect(vibrato_speed = 40, vibrato_depth = 100  / 2) ]

    def update_voice(self, voice, now, elapsed_ms, extra):
        VoiceUtils.clear_waves(voice)
        voice.pulse = True

        voice.attack = 10
        voice.decay = 5
        voice.sustain = 5
        voice.release = 10

        note = extra #passed in midi note
        VoiceUtils.set_frequency(voice, note.midi_note, now, self.effects)

        release_after_ms = VoiceUtils.get_duration(voice)
        if release_after_ms < elapsed_ms:
            voice.gate = False
            return False
        else:
            return True



#drums
class Instrument3:

    def update_voice(self, voice, now, elapsed_ms, extra):
        VoiceUtils.clear_waves(voice)
        voice.noise = True

        voice.attack = 0
        voice.decay = 0
        voice.sustain = 5
        voice.release = 6

        note = extra #passed in midi note
        VoiceUtils.set_frequency(voice, note.midi_note, now)

        release_after_ms = 300/4
        if release_after_ms < elapsed_ms:
            voice.gate = False
            return False
        else:
            return True


