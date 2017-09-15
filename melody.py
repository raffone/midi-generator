import time
import rtmidi
import random as r
from notes import *


class Melody:

    def __init__(self, scale, tempo, lengths):

        self.midiout = rtmidi.MidiOut()
        self.midiout.open_virtual_port("Midi Melody")

        self.stack = {}
        self.scale = scale
        self.tempo = tempo
        self.lengths = lengths

    def get_note(self, name='C', root=3, span=False, random=False):

        # Se random scegli a caso nella scala
        if random is True:
            name = r.choice(self.scale)

        index = self.scale.index(name)

        # Pitch per l'altezza della nota
        if span == 4:
            pitch = r.randrange(root - 2, root + 2)
        elif span == 3:
            pitch = r.randrange(root - 1, root + 2)
        elif span == 2:
            pitch = r.randrange(root, root + 2)
        else:
            pitch = root

        # Valore midi
        value = notes[pitch][name]

        return {'name': name, 'value': value, 'pitch': pitch, 'index': index}

    def play_note(self, note=60, duration=1, velocity=127):

        # Suona nota.
        # print '%s nuova, aggiungo' % (note)
        self.midiout.send_message([0x90, note, velocity])

        # Aggiungi allo stack per la cancellazione allo scadere della durata
        now = time.time()
        self.stack[note] = now + duration

    def clear_expired(self):

        # print self.stack
        now = time.time()
        for note in self.stack.keys():
            if self.stack[note] < now:
                # print '%s vecchia, cancello' % (note)
                self.midiout.send_message([0x80, note, 0])
                del self.stack[note]
                # self.stack.remove(note);

    def clear_all(self):
        for note in self.stack.keys():
            self.midiout.send_message([0x80, note, 0])
            del self.stack[note]

    def generate(self):
        # chord = []
        chance = r.random()

        # Se stack vuoto
        case1 = len(self.stack) == 0 and chance >= .1

        # Se stack non vuoto e non supeiore a 3
        case2 = len(self.stack) != 0 and len(self.stack) <= 3 and chance >= .7

        if (case1 or case2):
            # Prima nota random
            note = self.get_note(root=4, span=3, random=True)

            # Evito una nota gia nello stack
            if note['value'] in self.stack:
                return

            # duration = r.choice(self.lengths[0:3])
            self.play_note(note['value'], r.choice(
                self.lengths[:5]), r.randint(70, 90))

            # # Se durata minima di un battito possibilita' di diventare multinota
            if chance >= .8:
                var1 = r.choice([2, 5])
                # var1 = r.randint(2, 5)
                index1 = self.scale[(note['index'] + var1) % len(self.scale)]
                note1 = self.get_note(index1, root=3, span=2, )
                self.play_note(note1['value'], r.choice(
                    self.lengths[4:]), r.randint(90, 110))

            if chance >= .9:
                var2 = r.choice([2, 5])
                # var2 = r.randint(2, 5)
                index2 = self.scale[(note['index'] + var2) % len(self.scale)]
                note2 = self.get_note(index1, root=2, span=1, )
                self.play_note(note2['value'], r.choice(
                    self.lengths[7:]), r.randint(60, 100))

        # Rimuovi note finite
        self.clear_expired()

        # print len(self.stack)
        # print '---'

        # time.sleep(duration)

        # Sleep dell'intervallo minimo tra note
        # time.sleep(self.lengths[0])
