import time
import rtmidi
from rtmidi.midiconstants import *
import random as r

from notes import *
from instrument import Instrument

class Percussions(Instrument):

    def __init__(self, settings, name='V. Percussions'):
        Instrument.__init__(self, settings, name)

        # self.midiout = rtmidi.MidiOut()
        # self.midiout.open_virtual_port("Midi Percussions")

        # self.stack = {}
        # self.tempo = tempo
        # self.lengths = lengths

        # Parti
        self.kick = self.generate_euclidean_rhythm(32, 4)
        self.snare = self.generate_euclidean_rhythm(32, 4, 2)
        self.hihat1 = self.generate_euclidean_rhythm(32, 10, 2)
        # self.kick = self.generate_euclidean_rhythm(32, 5)
        # self.snare = self.generate_euclidean_rhythm(32, 4, 2)
        # self.hihat1 = self.generate_euclidean_rhythm(32, 7, 2)
        # self.hihat2 = self.generate_euclidean_rhythm(32, 3, 3)
        self.perc1 = self.generate_random_rhythm(32, 8)
        self.perc2 = self.generate_random_rhythm(32, 8)
        # self.misc1 = self.generate_euclidean_rhythm(32, 5, 6)
        # self.misc2 = self.generate_euclidean_rhythm(32, 4, 7)

        self.index = -1

        # self.test = self.generate_random_rhythm(32, 8)

    def play_note(self, note, rhythm, velocity=127):

        # verifica se suonare o no la nota in base al ritmo
        if rhythm[(self.index + 1) % len(rhythm)] != 0:


            # Suona nota.
            # print '%s nuova, aggiungo' % (note)
            self.midiout.send_message([NOTE_ON, note, velocity])

            # Aggiungi allo stack per la cancellazione allo scadere della durata
            now = time.time()
            self.stack[note] = now + self.lengths[0]

    def generate(self):
        # chord = []
        chance = r.random()


        # self.generate_random_rhythm(32, 8)
        # print self.test

        # print '<'
        # print self.kick
        # print self.snare
        # print self.hihat1
        # print self.hihat2
        # print self.perc1
        # print self.perc2
        # print self.misc1
        # print self.misc2
        # print '>'

        self.play_note(notes[2]['C'], self.kick)
        self.play_note(notes[2]['D#'], self.snare)
        self.play_note(notes[2]['F#'], self.hihat1)
        # self.play_note(notes[2]['A#'], self.hihat2)
        self.play_note(notes[2]['A'], self.perc1)
        self.play_note(notes[2]['G'], self.perc2)
        # self.play_note(notes[2]['C'], self.misc1)
        # self.play_note(notes[2]['C'], self.misc2)

        # Incremento indice
        self.index = self.index + 1

        # Rimuovi note finite
        self.clear_expired()
