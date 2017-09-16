import time
import rtmidi
from notes import *
from melody import Melody
from percussions import Percussions
from sequencer import Sequencer


def calc_bpm(tempo=120.0):
    return (60.0 / float(tempo))

# SETUP MUSIC
# ----------------------------------------------------------------------------
scale = scales['minor']['D#']
bpm = 80
base_interval = calc_bpm(bpm)
intervals = [base_interval * 0.25, base_interval * 0.33, base_interval * 0.50,
             base_interval * 0.75, base_interval * 0.66, base_interval,
             base_interval * 1.25, base_interval * 1.50, base_interval * 1.75,
             base_interval * 2.00, base_interval * 2.50, base_interval * 3.00]

settings = {'scale': scale, 'bpm': bpm, 'intervals': intervals}

# SEQUENCER
# ----------------------------------------------------------------------------
melody = Melody(settings)
percussions = Percussions(settings)
sequencer = Sequencer(settings, [melody, percussions])

try:
    sequencer.play()
except (KeyboardInterrupt, SystemExit):
    sequencer.stop()
