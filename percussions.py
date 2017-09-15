import time
import rtmidi
import random as r
from notes import *
from euclidean_rhythm import bjorklund


class Percussions:

    def __init__(self, tempo, lengths):

        self.midiout = rtmidi.MidiOut()
        self.midiout.open_virtual_port("Midi Percussions")

        self.stack = {}
        self.tempo = tempo
        self.lengths = lengths

        # Parti
        self.kick = bjorklund(32, 4)
        self.snare = bjorklund(32, 4, 2)
        self.hihat1 = bjorklund(32, 10, 2)
        # self.kick = bjorklund(32, 5)
        # self.snare = bjorklund(32, 4, 2)
        # self.hihat1 = bjorklund(32, 7, 2)
        # self.hihat2 = bjorklund(32, 3, 3)
        self.perc1 = self.generate_random_rhythm(32, 8)
        self.perc2 = self.generate_random_rhythm(32, 8)
        # self.misc1 = bjorklund(32, 5, 6)
        # self.misc2 = bjorklund(32, 4, 7)

        self.index = -1

        # self.test = self.generate_random_rhythm(32, 8)

    def random_subset(self,  iterator, K ):
        result = []
        N = 0

        for item in iterator:
            N += 1
            if len( result ) < K:
                result.append( item )
            else:
                s = int(r.random() * N)
                if s < K:
                    result[ s ] = item

        return result

    def generate_random_rhythm(self, length=32, count=8):
        pattern = [0 for i in range(length)]
        indexes = self.random_subset([i for i in range(length)], count)

        for i in indexes:
            pattern[i] = 1

        return pattern

    def play_note(self, note, rhythm, velocity=127):

        # verifica se suonare o no la nota in base al ritmo
        if rhythm[(self.index + 1) % len(rhythm)] != 0:


            # Suona nota.
            # print '%s nuova, aggiungo' % (note)
            self.midiout.send_message([0x90, note, velocity])

            # Aggiungi allo stack per la cancellazione allo scadere della durata
            now = time.time()
            self.stack[note] = now + self.lengths[0]

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


        # Se stack vuoto
        # note = self.get_note(root=3, random=True)

        # duration = r.choice(self.lengths[0:3])
        # self.play_note(note['value'], r.choice(self.lengths[:3]), r.randint(70, 90))


        # Rimuovi note finite
        self.clear_expired()

        # time.sleep(duration)

        # Sleep dell'intervallo minimo tra note
        # time.sleep(self.lengths[2])
