import time
import rtmidi
from rtmidi.midiconstants import *
import random as r

from notes import *
from instrument import Instrument


class Percussions(Instrument):

    def __init__(self, settings, name='V. Percussions'):
        Instrument.__init__(self, settings, name)

        # Kit
        self.kit = {
            'kick': self.generate_rhythm('kick', {
                'steps': {'count': 32},
                'pulses': {'count': 2}
            }),
            'snare': self.generate_rhythm('snare', {
                'steps': {'count': 32},
                'pulses': {'count': 4},
                'shift': {'count': 4}
            }),
            'hihat1': self.generate_rhythm('hihat1', {
                'steps': {'min': 16, 'max': 32},
                'pulses': {'min': 4, 'max': 8},
                'random': True,
                'mutating': True,
            }),
            'perc1': self.generate_rhythm('perc1', {
                'steps': {'min': 16, 'max': 32, },
                'pulses': {'min': 4, 'max': 8, },
                'random': True,
                'mutating': True,
            }),
            'perc2': self.generate_rhythm('perc2', {
                'steps': {'min': 16, 'max': 32},
                'pulses': {'min': 4, 'max': 8},
                'random': True,
                'mutating': True,
            }),
        }

        self.index = -1

    def play_note(self, note, rhythm, velocity=127):
        name = rhythm['name']
        pattern = rhythm['pattern']
        settings = rhythm['settings']

        # index = (self.index + 1) % rhythm['length']
        index = (rhythm['index'] + 1) % rhythm['length']

        # verifica se suonare o no la nota in base al ritmo
        if pattern[index] != 0:

            # Suona nota.
            self.midiout.send_message([NOTE_ON, note, velocity])

            # Aggiungi allo stack per la cancellazione allo scadere della
            # durata
            now = time.time()
            self.stack[note] = now + self.lengths[0]

        # if name == 'perc2':
        #     print rhythm['index'] + 2

        # Se ritmo random e mutante e alla fine del pattern -> rigenera
        if ('random' in settings and settings['random'] == True
                and 'mutating' in settings and settings['mutating'] == True
                and index == rhythm['length'] - 1):

            # print('pattern finito', name, pattern, settings['random'], settings['mutating'], rhythm['length'] - 1, index)
            print('rigenero', name)

            self.kit[name] = self.generate_rhythm(name, settings)
            # print self.kit[name]['length'], self.kit[name]['pattern']

        # Incrementa index pattern
        rhythm['index'] += 1

    def generate(self):
        # chord = []
        chance = r.random()

        # self.generate_random_rhythm(32, 8)
        # print self.testottimo

        # print '<'
        # print self.kit
        # print self.snare
        # print self.hihat1
        # # print self.hihat2
        # print self.perc1
        # print self.perc2
        # print self.misc1
        # print self.misc2
        # print '>'

        self.play_note(notes[2]['C'], self.kit['kick'])
        self.play_note(notes[2]['D#'], self.kit['snare'])
        self.play_note(notes[2]['F#'], self.kit['hihat1'])
        # self.play_note(notes[2]['A#'], self.hihat2)
        self.play_note(notes[2]['A'], self.kit['perc1'])
        self.play_note(notes[2]['G'], self.kit['perc2'])

        # Incremento indice
        # self.index = self.index + 1

        # Rimuovi note finite
        self.clear_expired()
