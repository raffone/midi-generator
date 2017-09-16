import time
import rtmidi
from rtmidi.midiconstants import *
import random as r
from notes import *
from instrument import Instrument

class Controls(Instrument):

    def __init__(self, settings, name='V. Controls'):
        Instrument.__init__(self, settings, name)

        # self.midiout = rtmidi.MidiOut()
        # available_ports = self.midiout.get_ports()

        # if available_ports:
        #     self.midiout.open_port(0)
        # else:
        #     self.midiout.open_virtual_port("Virtual Output")

        # self.stack = {}

    # def clear_expired(self):
    #     now = time.time()
    #     for note in self.stack.keys():
    #         if self.stack[note] < now:
    #             self.midiout.send_message([NOTE_OFF, note, 0])
    #             del self.stack[note]

    # def clear_all(self):
    #     for note in self.stack.keys():
    #         self.midiout.send_message([NOTE_OFF, note, 0])
    #         del self.stack[note]


    def play_note(self, note=60, duration=1, velocity=127):
        # print 'GINo'

        # Suona nota.
        # print '%s nuova, aggiungo' % (note)
        self.midiout.send_message([NOTE_ON, note, velocity])

        # Aggiungi allo stack per la cancellazione allo scadere della durata
        now = time.time()
        self.stack[note] = now + duration


    def generate(self):

        # self.play_note(notes[1]['C'])

        # Rimuovi note finite
        self.clear_expired()
