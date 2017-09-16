import time
import rtmidi
from notes import *
from melody import Melody
from percussions import Percussions
from controls import Controls


def bpm(tempo=120.0):
    return (60.0 / float(tempo))

TEMPO = bpm(80.0)

# SETUP MUSIC
# ----------------------------------------------------------------------------
settings = {
    'scale': scales['minor']['D#'],
    'tempo': TEMPO,
    'lengths': [TEMPO * 0.25, TEMPO * 0.33, TEMPO * 0.50, TEMPO * 0.75, TEMPO * 0.66, TEMPO,
                TEMPO * 1.25, TEMPO * 1.50, TEMPO * 1.75, TEMPO * 2.00, TEMPO * 2.5],
}

print settings

# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------

# print TEMPO
# print BASE_DURATIONS
# MAIN LOOP
# ----------------------------------------------------------------------------

melody = Melody(settings)
percussions = Percussions(settings)
controls = Controls(settings)


try:
    time.sleep(2)
    # controls.play_note(notes[1]['C'], 0.1)
    # controls.play_note(notes[1]['D'])
    # time.sleep(5)

    callcount = 0
    interval = 15. / 80
    started = time.time()

    while True:

        # print time.time()
        melody.generate()
        percussions.generate()
        controls.generate()
        # print time.time()

        # print melody.stack
        # print percussions.stack
        # print controls.stack
        print '---'

        callcount = callcount + 1
        # Compensate for drift:
        # calculate the time when the worker should be called again.
        nexttime = started + callcount * interval
        timetowait = max(0, nexttime - time.time())

        time.sleep(timetowait)

except (KeyboardInterrupt, SystemExit):
    controls.play_note(notes[1]['C#'])

    melody.clear_all()
    del melody.midiout

    percussions.clear_all()
    del percussions.midiout
