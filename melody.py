import time
import rtmidi
from rtmidi.midiconstants import *
import random as r
from notes import *
from instrument import Instrument


class Melody(Instrument):

    def __init__(self, name, global_settings, settings):
        Instrument.__init__(self, global_settings, name)

        self.settings = settings

    def get_note(self, name='C', root=3, span=False, random=False):

        # Se random scegli a caso nella scala
        if type(name) is list:
            name = r.choice(name)
        elif random is True:
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
        self.midiout.send_message([NOTE_ON, note, velocity])

        # Aggiungi allo stack per la cancellazione allo scadere della durata
        now = time.time()
        self.stack[note] = now + duration

    def generate(self):
        # chord = []
        chance = 1.00 - r.random()

        # print chance
        # print 1.00 - chance

        main_note = ''

        # TODO: migliorare il passaggio da una nota all'altra per evitare
        # intervalli esagerati
        if('melody' in self.settings):
            if (len(self.stack) == 0 and self.settings['melody']['chance'] >= chance):

                # Prima nota random
                # Se e' stata passata una lista di note usa quelle
                if ('notes' in self.settings['melody']):
                    main_note = self.get_note(name=self.settings['melody']['notes'],
                                              root=self.settings['melody']['root'],
                                              span=self.settings['melody']['span'],
                                              random=self.settings['melody']['random'])
                else:
                    main_note = self.get_note(root=self.settings['melody']['root'],
                                              span=self.settings['melody']['span'],
                                              random=self.settings['melody']['random'])

                # Se richiesto evito di ripetere note attualmente suonate
                if not self.settings['melody']['note_repeat']:
                    if main_note['value'] in self.stack:
                        return

                # Suona nota
                self.play_note(note=main_note['value'],
                               duration=r.choice(self.settings['melody']['length']),
                               velocity=r.randint(self.settings['melody']['velocity']['min'],
                                                  self.settings['melody']['velocity']['max']))

        if('chord' in self.settings):
            if len(self.stack) <= len(self.settings['chord']):
                for chord in self.settings['chord']['notes']:
                    # print 'chord'
                    # print chord

                    if chord['chance'] >= chance:
                        # print main_note
                        if 'follow_main_note' in chord and main_note != '':
                            var = r.choice(chord['offset'])
                            index = self.scale[(main_note['index'] + var) % len(self.scale)]
                        else:
                            index = r.choice(self.scale)

                        note = self.get_note(name=index,
                                             root=chord['root'],
                                             span=chord['span'],
                                             random=chord['random'])

                        self.play_note(note=note['value'],
                                       duration=r.choice(chord['length']),
                                       velocity=r.randint(chord['velocity']['min'],
                                                          chord['velocity']['max']))
