import time
import rtmidi
from rtmidi.midiconstants import *
import random as r
from notes import *
from instrument import Instrument


class Controls(Instrument):

    def __init__(self, settings, name='V. Controls'):
        Instrument.__init__(self, settings, name)

    def play_note(self, note=60, duration=1, velocity=127):
        # print 'GINo'

        # Suona nota.
        # print '%s nuova, aggiungo' % (note)
        self.midiout.send_message([NOTE_ON, note, velocity])

        # Aggiungi allo stack per la cancellazione allo scadere della durata
        now = time.time()
        self.stack[note] = now + duration

    def generate(self):
        pass

        # self.play_note(notes[1]['C'])

        # # Rimuovi note finite
        # self.clear_expired()
