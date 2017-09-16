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
# intervals = [base_interval * 0.25, base_interval * 0.33, base_interval * 0.50,
#              base_interval * 0.75, base_interval * 0.66, base_interval,
#              base_interval * 1.25, base_interval * 1.50, base_interval * 1.75, ]
intervals = [base_interval * 0.25, base_interval * 0.50, base_interval * 0.75, base_interval,
             base_interval * 1.25, base_interval * 1.50, base_interval * 1.75, base_interval * 2.00, ]


settings = {'scale': scale, 'bpm': bpm, 'intervals': intervals}

# SEQUENCER
# ----------------------------------------------------------------------------
melody = Melody(settings)
drums = Percussions('Drums', settings, [{
    'name': 'kick',
    'note': notes[2]['C'],
    'steps': {'count': 32},
    'pulses': {'count': 2}
}, {
    'name': 'snare',
    'note': notes[2]['E'],
    'steps': {'count': 32},
    'pulses': {'count': 4},
    'shift': {'count': 4}
}, {
    'name': 'hihat1',
    'note': notes[2]['G#'],
    'steps': {'min': 16, 'max': 32},
    'pulses': {'min': 4, 'max': 8},
    'random': True,
    'mutating': True,
}, {
    'name': 'hihat2',
    'note': notes[2]['B'],
    'steps': {'min': 16, 'max': 32},
    'pulses': {'min': 4, 'max': 8},
    'random': True,
    'mutating': True,
}])

glitch = Percussions('Glitch', settings, [{
    'name': 'glitch1', 'note': notes[2]['C'],
    'steps': {'count': 64}, 'pulses': {'min': 4, 'max': 8},
    'random': True, 'mutating': True,
}, {
    'name': 'glitch2', 'note': notes[2]['C#'],
    'steps': {'count': 64}, 'pulses': {'min': 4, 'max': 8},
    'random': True, 'mutating': True,
}, {
    'name': 'glitch3', 'note': notes[2]['D'],
    'steps': {'count': 64}, 'pulses': {'min': 4, 'max': 8},
    'random': True, 'mutating': True,
}, {
    'name': 'glitch4', 'note': notes[2]['E'],
    'steps': {'count': 64}, 'pulses': {'min': 4, 'max': 8},
    'random': True, 'mutating': True,
}, {
    'name': 'glitch5', 'note': notes[2]['F'],
    'steps': {'count': 64}, 'pulses': {'min': 4, 'max': 8},
    'random': True, 'mutating': True,
}, {
    'name': 'glitch6', 'note': notes[2]['F'],
    'steps': {'count': 64}, 'pulses': {'min': 4, 'max': 8},
    'random': True, 'mutating': True,
}])


# glitch = Percussions(name='Glitch')

sequencer = Sequencer(settings, [melody, drums, glitch])

try:
    sequencer.play()
except (KeyboardInterrupt, SystemExit):
    sequencer.stop()
