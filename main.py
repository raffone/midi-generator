import rtmidi
from notes import *
from melody import Melody

# SETUP
# ----------------------------------------------------------------------------


# FUNCTIONS
# ----------------------------------------------------------------------------


def current_time():
    return int(round(time.time()))


def bpm(tempo=120.0):
    return (60.0 / float(tempo))


# SETUP MUSIC
# ----------------------------------------------------------------------------
# SCALE = scales['minor']['D#']
SCALE = scales['minor']['C']
TEMPO = bpm(80)
BASE_DURATIONS = [TEMPO * 0.25, TEMPO * 0.33, TEMPO * 0.50, TEMPO * 0.75, TEMPO * 0.66, TEMPO,
                  TEMPO * 1.25, TEMPO * 1.50, TEMPO * 1.75, TEMPO * 2.00, TEMPO * 2.5]

# MAIN LOOP
# ----------------------------------------------------------------------------

melody = Melody(SCALE, TEMPO, BASE_DURATIONS)

try:
    while True:
        melody.generate_melody()

except (KeyboardInterrupt, SystemExit):
    melody.clear_all_notes()
    del midiout

