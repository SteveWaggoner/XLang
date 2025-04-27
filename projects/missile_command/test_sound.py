#!/usr/bin/env python3.8


##################################################################

from sound import SoundManager, MusicManager, set_filter
from music import Instrument1, Instrument2, Instrument3, SongA
from sfx import ExplosionSound

from game_display import Display
import window_sdl2
import time

def main():

    sfx = SoundManager()
    music = MusicManager(sfx)

    music.set_track(1, Instrument1(), SongA.base_notes)
    music.set_track(2, Instrument2(), SongA.notes)
    music.set_track(3, Instrument3(), SongA.drum_notes)

    display = Display(window_sdl2.Window("Missile Command", mode="VGA"))

    i = 0

    print("ready")
    while True:

        set_filter(sfx.sid)

        now = int(time.time() * 1000)

        display.window.poll_events()
        key = display.check_key()
        if key is not None:
            if key == 32:
                print("space bar "+str(i))
                sfx.start(now, ExplosionSound(), i)
                i = i + 1
                if i > 2:
                    i = 0

            elif key == 97:
                print("letter a")
                print(sfx.sid.voices[1])
            elif key == 122:
                print("letter z")
            else:
                print(key)
                break

        music.tick(now)
        sfx.tick(now)

        time.sleep(0.001)



if __name__=="__main__":
    main()

