import time
import rtmidi
from rtmidi.midiconstants import *
import random as r

from notes import *
from instrument import Instrument


class Percussions(Instrument):

    def __init__(self, name, global_settings, settings):
        Instrument.__init__(self, global_settings, name)

        self.kit = {}

        for part in settings:
            self.kit[part['name']] = self.generate_rhythm(part)

        self.index = -1

    def play_note(self, note, rhythm, velocity=127):
        settings = rhythm['settings']
        pattern = rhythm['pattern']
        name = settings['name']

        index = (rhythm['index'] + 1) % len(rhythm['pattern'])

        # verifica se suonare o no la nota in base al ritmo
        if pattern[index] != 0:

            # Suona nota.
            self.midiout.send_message([NOTE_ON, note, velocity])

            # Aggiungi allo stack per la cancellazione allo scadere della durata
            now = time.time()
            self.stack[note] = now + self.intervals[0]

        # Se ritmo random e mutante e alla fine del pattern -> rigenera
        if ('random' in settings and settings['random'] == True
                and 'mutating' in settings and settings['mutating'] == True
                and index == len(rhythm['pattern']) - 1):

            print('rigenero', name)

            self.kit[name] = self.generate_rhythm(settings)

        # Incrementa index pattern
        rhythm['index'] += 1

    def generate(self):

        for name in self.kit:
            # print self.kit[name]['settings']['note']
            self.play_note(self.kit[name]['settings']['note'], self.kit[name])
