import time
import rtmidi
import random
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


def get_random_note(scale, root=3, span=False):
    note = random.choice(scale)

    if span == 4:
        return notes[random.randrange(root - 2, root + 2)][note]
    elif span == 3:
        return notes[random.randrange(root - 1, root + 2)][note]
    elif span == 2:
        return notes[random.randrange(root, root + 2)][note]
    else:
        return notes[root][note]


def play_note(note=60, duration=1, velocity=127):
    global STACK

    # Se esiste gia interrompi la nota prima di suonarla
    # midiout.send_message([0x80, note, 0])

    # Se stai gia suonando la stessa nota skippa
    if note in STACK:
        return

    # Suona nota
    midiout.send_message([0x90, note, velocity])

    # Aggiungi allo stack per la cancellazione allo scadere della durata
    now = time.time()
    # STACK.append((0x90, now, now + duration))
    STACK[note] = now + duration

    # time.sleep(duration)
    # midiout.send_message([0x80, note, 0])


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
    note = get_random_note(SCALE, 4, 1)
    duration = random.uniform(TEMPO / 4, TEMPO * 2)
    play_note(note, duration, 127)
    print(note, duration, 127)

    clear_expired_notes()

    print '*'
    time.sleep(duration)

def generate_chords():
	pass


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
SCALE = scales['pentatonic']['G#']
TEMPO = bpm(110)
SPEED = 1 / 4

# MAIN LOOP
# ----------------------------------------------------------------------------

# print TEMPO, TEMPO * (1 / 4), TEMPO / 2, TEMPO / 4
# i = 10
while True:
    generate_melody()


del midiout
