import time
import rtmidi
import random as r
from notes import *

# SETUP
# ----------------------------------------------------------------------------
STACK = {}

# FUNCTIONS
# ----------------------------------------------------------------------------


def current_time():
    return int(round(time.time()))


def bpm(tempo=120.0):
    return (60.0 / float(tempo))


def get_note(name='C', root=3, span=False, random=False):
    global SCALE

    # Se random scegli a caso nella scala
    if random is True:
        name = r.choice(SCALE)

    index = SCALE.index(name)

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
    value = notes[root][name]

    return {'name': name, 'value': value, 'pitch': pitch, 'index': index}


def play_note(note=60, duration=1, velocity=127):
    global STACK

    # Se esiste gia interrompi la nota prima di suonarla
    # midiout.send_message([0x80, note, 0])

    # Se stai gia suonando la stessa nota skippa
    # if note in STACK:
    #     return

    # Suona nota.\
    print '%s nuova, aggiungo' % (note)
    midiout.send_message([0x90, note, velocity])

    # Aggiungi allo stack per la cancellazione allo scadere della durata
    now = time.time()
    STACK[note] = now + duration


def clear_expired_notes():
    global STACK
    # print STACK
    now = time.time()
    for note in STACK.keys():
        if STACK[note] < now:
            print '%s vecchia, cancello' % (note)
            midiout.send_message([0x80, note, 0])
            del STACK[note]
            # STACK.remove(note);


def generate_melody():
    # chord = []
    chance = r.random()

    # Prima nota random
    note = get_note(root=4, span=2, random=True)
    if note['value'] in STACK:
        return


    duration = r.choice(BASE_DURATIONS)
    play_note(note['value'], duration, 127)

    # Se durata minima di un battito possibilita' di diventare multinota
    if duration >= TEMPO and chance > 0.5:
    # if duration >= TEMPO:
        var1 = r.randint(2, 5)
        index1 = SCALE[(note['index'] + var1) % len(SCALE)]
        note1 = get_note(index1, root=2, span=1, )
        play_note(note1['value'], duration, 80)

        var2 = r.randint(2, 5)
        index2 = SCALE[(note['index'] + var2) % len(SCALE)]
        note2 = get_note(index1, root=2, span=1, )
        play_note(note2['value'], duration, 80)

    clear_expired_notes()

    print '*'
    time.sleep(duration)

# def generate_chords()
    # pass


# SETUP MIDI
# ----------------------------------------------------------------------------
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")


# SETUP MUSIC
# ----------------------------------------------------------------------------
# SCALE = scales['minor']['D#']
SCALE = scales['pentatonic']['D#']
TEMPO = bpm(60)
# BASE_DURATIONS = [TEMPO * 0.25, TEMPO * 0.5,
#                   TEMPO * 0.75, TEMPO, TEMPO * 1.5, TEMPO * 2]
BASE_DURATIONS = [TEMPO, TEMPO * 1.5, TEMPO * 2, TEMPO, TEMPO * 2.5, TEMPO * 3, TEMPO, TEMPO * 3.5, TEMPO * 4]

# MAIN LOOP
# ----------------------------------------------------------------------------

# print TEMPO, TEMPO * (1 / 4), TEMPO / 2, TEMPO / 4
# i = 10
while True:
    generate_melody()
    # play_note(60, TEMPO, 127)
    # time.sleep(TEMPO)


del midiout
