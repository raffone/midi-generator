import time
import rtmidi
from notes import *
from melody import Melody
from percussions import Percussions

def bpm(tempo=120.0):
    return (60.0 / float(tempo))



# SETUP MUSIC
# ----------------------------------------------------------------------------
SCALE = scales['minor']['C']
TEMPO = bpm(80.0)
BASE_DURATIONS = [TEMPO * 0.25, TEMPO * 0.33, TEMPO * 0.50, TEMPO * 0.75, TEMPO * 0.66, TEMPO,
                  TEMPO * 1.25, TEMPO * 1.50, TEMPO * 1.75, TEMPO * 2.00, TEMPO * 2.5]

# print TEMPO
# print BASE_DURATIONS
# MAIN LOOP
# ----------------------------------------------------------------------------

melody = Melody(SCALE, TEMPO, BASE_DURATIONS)
percussions = Percussions(TEMPO, BASE_DURATIONS)

try:
    while True:
        melody.generate()
        percussions.generate()

        print '---'

        time.sleep(BASE_DURATIONS[0])

except (KeyboardInterrupt, SystemExit):
    melody.clear_all()
    del melody.midiout

    percussions.clear_all()
    del percussions.midiout

