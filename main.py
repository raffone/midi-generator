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
    value = notes[pitch][name]

    return {'name': name, 'value': value, 'pitch': pitch, 'index': index}


def play_note(note=60, duration=1, velocity=127):
    global STACK

    # Suona nota.
    # print '%s nuova, aggiungo' % (note)
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
            # print '%s vecchia, cancello' % (note)
            midiout.send_message([0x80, note, 0])
            del STACK[note]
            # STACK.remove(note);

def clear_all_notes():
    for note in STACK.keys():
        midiout.send_message([0x80, note, 0])
        del STACK[note]

def generate_melody():
    # chord = []
    chance = r.random()

    # Se stack vuoto
    case1 =  len(STACK) == 0 and chance >= .1

    # Se stack non vuoto e non supeiore a 3
    case2 =  len(STACK) != 0 and len(STACK) <= 3 and chance >= .7

    if (case1 or case2):
        # Prima nota random
        note = get_note(root=4, span=3, random=True)

        # Evito una nota gia nello stack
        if note['value'] in STACK:
            return

        # duration = r.choice(BASE_DURATIONS[0:3])
        play_note(note['value'], r.choice(BASE_DURATIONS[:5]), r.randint(70, 90))

        # # Se durata minima di un battito possibilita' di diventare multinota
        if chance >= .8:
            var1 = r.choice([2, 5])
            # var1 = r.randint(2, 5)
            index1 = SCALE[(note['index'] + var1) % len(SCALE)]
            note1 = get_note(index1, root=3, span=2, )
            play_note(note1['value'], r.choice(BASE_DURATIONS[4:]), r.randint(90, 110))

        if chance >= .9:
            var2 = r.choice([2, 5])
            # var2 = r.randint(2, 5)
            index2 = SCALE[(note['index'] + var2) % len(SCALE)]
            note2 = get_note(index1, root=2, span=1, )
            play_note(note2['value'], r.choice(BASE_DURATIONS[7:]), r.randint(60, 100))

    # Rimuovi note finite
    clear_expired_notes()

    print len(STACK)
    print '---'

    # time.sleep(duration)

    # Sleep dell'intervallo minimo tra note
    time.sleep(BASE_DURATIONS[0])

# def generate_chords()
    # pass


# SETUP MIDI
# ----------------------------------------------------------------------------
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("Midi Generator")


# SETUP MUSIC
# ----------------------------------------------------------------------------
# SCALE = scales['minor']['D#']
SCALE = scales['minor']['C']
TEMPO = bpm(80)
BASE_DURATIONS = [TEMPO * 0.25, TEMPO * 0.33, TEMPO * 0.50, TEMPO * 0.75, TEMPO * 0.66, TEMPO,
                  TEMPO * 1.25, TEMPO * 1.50, TEMPO * 1.75, TEMPO * 2.00, TEMPO * 2.5]

# MAIN LOOP
# ----------------------------------------------------------------------------

try:
    while True:
        generate_melody()

except (KeyboardInterrupt, SystemExit):
    clear_all_notes()
    del midiout

