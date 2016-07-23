#!/usr/bin/env python3

from housepy import config, util
signals = util.load("signals.pkl")

from braid import *

YEARS = 1

core.log_midi = True
core.midi_out.throttle = 0.01
tempo(204)
# tempo(75)

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# roots =    [G2, G2, G2, G3, G3, G3, G4, G4]
# notes =    [1,  3,  5,  2,  6,  7,  4,  2]
roots =    [G2, G2, G2, G2, G3, G3, G3, G3, G4, G4, G4]
notes =    [1,  3,  5,  7,  2,  3,  4,  6,  2,  5, 7]
colors =   ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'brown', 'cyan', 'magenta', 'lightgreen', 'grey']
signals.reverse()

for s, signal in enumerate(signals):
    if s == len(channels):
        break
    v = Voice(channels[s], rate=1, chord=(roots[s], LYD), sustain=True, controls={'volume': 20})

    f = signal_from_timeseries(signal)
    plot(f, color=colors[s])
    v.volume(0)    
    v.volume.tween(127, YEARS * 12 * 2, f, repeat=True, flip=False)

    v.play(notes[s])
    # v.play_at(5, notes[s])
    # v.set([notes[s]])

    
show_plots()
play()

