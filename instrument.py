import time
import rtmidi
from rtmidi.midiconstants import *
import random as r
from notes import *


class Instrument:
    def __init__(self, settings, name='V. Instrument'):
        self.midiout = rtmidi.MidiOut()
        # self.midiout.open_virtual_port("Midi Melody")
        available_ports = self.midiout.get_ports()
        # print available_ports
        # if available_ports:
        #     self.midiout.open_port(port)
        # else:
        self.midiout.open_virtual_port(name)

        self.stack = {}
        self.scale = settings['scale']
        self.tempo = settings['tempo']
        self.lengths = settings['lengths']

    def clear_expired(self):
        now = time.time()
        for note in self.stack.keys():
            if self.stack[note] < now:
                self.midiout.send_message([NOTE_OFF, note, 0])
                del self.stack[note]

    def clear_all(self):
        for note in self.stack.keys():
            self.midiout.send_message([NOTE_OFF, note, 0])
            del self.stack[note]


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


    def generate_euclidean_rhythm(self, steps, pulses, shift=False):
        steps = int(steps)
        pulses = int(pulses)
        if pulses > steps:
            raise ValueError
        pattern = []
        counts = []
        remainders = []
        divisor = steps - pulses
        remainders.append(pulses)
        level = 0
        while True:
            counts.append(divisor / remainders[level])
            remainders.append(divisor % remainders[level])
            divisor = remainders[level]
            level = level + 1
            if remainders[level] <= 1:
                break
        counts.append(divisor)

        def build(level):
            if level == -1:
                pattern.append(0)
            elif level == -2:
                pattern.append(1)
            else:
                for i in xrange(0, counts[level]):
                    build(level - 1)
                if remainders[level] != 0:
                    build(level - 2)

        build(level)
        i = pattern.index(1)
        pattern = pattern[i:] + pattern[0:i]

        if shift:
            pattern = pattern[-shift:] + pattern[:-shift]

        return pattern