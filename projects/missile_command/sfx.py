#!/usr/bin/env python3.8

from sound import Sound, VoiceUtils

class ExplosionInstrument:

    def update_voice(self, voice, now, elapsed_ms, extra=None):

        VoiceUtils.clear_waves(voice)
        voice.noise = True

        voice.attack = 6
        voice.decay = 2
        #modify sustain later
        voice.release=8

        # explosion table
        ms_hz_db = [
                     (0,	 20,	120),
                     (10,	100,	130),
                     (20,	300,	135),
                     (50,	800,	125),
                     (100,	500,	110),
                     (200,	200,	95),
                     (300,	100,	85),
                     (500,	60,	    75),
                     (1000,	40,	    60),
                     (1500,	40,	    70),
                     (2000,	30,	    45)
                    ]

        # gunshot
        ms_hz_db2 = [
            (0,    50,  90),
            (2, 3000,    140),
            (4, 6000,    145),
            (6, 4500,    130),
            (10, 1000,    115),
            (20, 500, 100),
            (50, 250, 85),
            (100, 100, 70),
            (200, 80,  60),
            (500, 50,  50)]


        if elapsed_ms < 2500:

            # https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
            millis, hertz, dB = min(ms_hz_db, key=lambda x:abs(x[0]-elapsed_ms))
            voice.pitch_to_frequency(hertz)
            voice.sustain = int((dB / 140) * 16) # volume from 0 to 15
            return True
        else:
            voice.sustain = 0   #turn off sound
            return False

class ExplosionSound(Sound):
    def __init__(self):
        super().__init__(instrument=ExplosionInstrument(), is_sfx=True, extra=None)
