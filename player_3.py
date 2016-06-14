#!/usr/bin/env python3

from phenology import signals
from braid import *

YEARS = 5

core.log_midi = True
# tempo(204)
tempo(50)

channels = [1, 2, 3, 4, 5, 6, 7, 8]
roots =    [G0, G1, G1, G2, G2, G3, G3, G4, G4]
notes =    [1, 3, 5, 7, 9, 1, 2, 4]
colors =   ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'brown', 'cyan']
signals.reverse()

for s, signal in enumerate(signals):
    # if s == len(channels):
    #     break
    if s == 5:
        break
    v = Voice(channels[s], rate=1, chord=(roots[s], LYD), controls={'volume': 20})

    f = signal_from_timeseries(signal)
    plot(f, color=colors[s])
    v.volume(0)    
    v.volume.tween(127, YEARS * 12 * 2, f, repeat=True, flip=False)

    # f = signal_from_timeseries(onset_signals[s])
    # plot(f, color=colors[s])
    # v.boost(0)
    # v.boost.tween(127, 24, f, repeat=True, flip=False)

    v.play(notes[s])
    v.play_at(5, notes[s])


    
show_plots()
play()

