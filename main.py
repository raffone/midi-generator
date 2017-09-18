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


global_settings = {'scale': scale, 'bpm': bpm, 'intervals': intervals}

# SEQUENCER
# ----------------------------------------------------------------------------
melody = Melody('Melody', global_settings, {
    'type': ['melody', 'chord'],  # melody, chord
    'melody': {
        'chance': .9, 'note_repeat': False,
        'root': 4, 'span': 3, 'random': True,
        'velocity': {'min': 70, 'max': 90},
        'length': intervals[:5]
    },
    'chord': {
        'notes': [{
            'chance': .2,
            'root': 3, 'span': 2, 'random': False,
            'follow_main_note': True,
            'offset': [2, 5],
            'velocity': {'min': 90, 'max': 110},
            'length': intervals[4:]
        }, {
            'chance': .1,
            'root': 2, 'span': 1, 'random': False,
            'follow_main_note': True,
            'offset': [2, 5],
            'velocity': {'min': 60, 'max': 100},
            'length': intervals[4:]
        }]
    }
})
# ----------------------------------------------------------------------------
bass = Melody('Bass', global_settings, {
    'type': ['melody'],  # melody, chord
    'melody': {
        'chance': .1, 'note_repeat': False,
        'root': 2, 'span': 1, 'random': True,
        'velocity': {'min': 70, 'max': 90},
        'length': intervals[2:6]
    },
})
# ----------------------------------------------------------------------------
drums = Percussions('Drums', global_settings, [{
    'name': 'kick', 'note': notes[2]['C'],
    'steps': {'count': 16}, 'pulses': {'count': 1}
}, {
    'name': 'kick2', 'note': notes[2]['C#'],
    'steps': {'count': 32}, 'pulses': {'min': 2, 'max': 3},
    'random': True, 'mutating': True,
}, {
    'name': 'snare', 'note': notes[2]['E'],
    'steps': {'count': 32}, 'pulses': {'count': 4},
    'shift': {'count': 4}
}, {
    'name': 'snare2', 'note': notes[2]['E'],
    'steps': {'count': 32}, 'pulses': {'min': 1, 'max': 2},
    'random': True, 'mutating': True, 'velocity': 80,
}, {
    'name': 'snare3', 'note': notes[2]['F'],
    'steps': {'count': 8}, 'pulses': {'count': 1},
    'shift': {'count': 4}
}, {
    'name': 'hihat3', 'note': notes[2]['F#'],
    'steps': {'count': 32}, 'pulses': {'min': 1, 'max': 2},
    'random': True, 'mutating': True,
}, {
    'name': 'hihat1', 'note': notes[2]['G#'],
    'steps': {'min': 16, 'max': 32}, 'pulses': {'min': 2, 'max': 4},
    'random': True, 'mutating': True,
}, {
    'name': 'hihat2', 'note': notes[2]['B'],
    'steps': {'min': 16, 'max': 32}, 'pulses': {'min': 2, 'max': 4},
    'random': True, 'mutating': True,
}])

# ----------------------------------------------------------------------------


glitch = Percussions('Glitch', global_settings, [{
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

# ----------------------------------------------------------------------------

sequencer = Sequencer(global_settings, [melody, bass, drums, glitch])

try:
    sequencer.play()
except (KeyboardInterrupt, SystemExit):
    sequencer.stop()
