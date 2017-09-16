import time
import rtmidi
from rtmidi.midiconstants import *
import random as r
from notes import *
from instrument import Instrument
from controls import Controls


class Sequencer:

    def __init__(self, settings, instruments):
        self.instruments = instruments
        self.settings = settings
        self.controls = Controls(settings)

    def play(self):
        # Offset per setup virtualmidi
        time.sleep(2)

        # Base per calcolo timing
        self.callcount = 0
        self.interval = 15. / self.settings['bpm']
        self.started = time.time()

        # Main loop
        while True:
            for instrument in self.instruments:
                instrument.generate()
                instrument.clear_expired()
                print instrument.stack

            print '----'

            # Intervallo con calcolo del drift
            self.callcount += 1
            self.nexttime = self.started + self.callcount * self.interval
            self.timetowait = max(0, self.nexttime - time.time())
            time.sleep(self.timetowait)

    def stop(self):
        self.controls.play_note(notes[1]['C#'])

        for instrument in self.instruments:
            instrument.clear_all()
            del instrument.midiout
