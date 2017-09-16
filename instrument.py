import time
import rtmidi
from rtmidi.midiconstants import *
import random as r
from notes import *


class Instrument:

    def __init__(self, settings, name='V. Instrument'):
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_virtual_port(name)

        self.stack = {}
        self.scale = settings['scale']
        self.intervals = settings['intervals']

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

    def random_subset(self, iterator, K):
        result = []
        N = 0

        for item in iterator:
            N += 1
            if len(result) < K:
                result.append(item)
            else:
                s = int(r.random() * N)
                if s < K:
                    result[s] = item

        return result

    # Generatori ritmo
    def generate_rhythm(self, name, s):

        # print s
        # print name
        # print 'shift' in s

        # Steps
        if ('min' in s['steps']):
            steps = r.randint(s['steps']['min'], s['steps']['max'])
        else:
            steps = s['steps']['count']

        # Pulses
        if ('min' in s['pulses']):
            pulses = r.randint(s['pulses']['min'], s['pulses']['max'])
        else:
            pulses = s['pulses']['count']

        # Shifts
        if ('shift' in s):
            shift = s['shift']['count']
        else:
            shift = 0

        # print steps, pulses, shift

        # Genera ritmo
        if ('random' in s):
            pattern = self.generate_random_rhythm(steps, pulses)
        else:
            pattern = self.generate_euclidean_rhythm(steps, pulses, shift)

        # print pattern

        return {
            'name': name,
            'pattern': pattern,
            'length': len(pattern),
            'index': -1,
            'settings': s,

        }

    def generate_random_rhythm(self, steps=32, pulses=8):
        pattern = [0 for i in range(steps)]
        indexes = self.random_subset([i for i in range(steps)], pulses)

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
