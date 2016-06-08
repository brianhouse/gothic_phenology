#!/usr/bin/env python3

from main import signals
from braid import *

core.log_midi = False
tempo(204)

def b(n):
    def f (v):
        v.note_velocity(1.0)
        return n
    return f

def p(n):
    def f(v):
        v.note_velocity(0.6)
        return n
    return f

signals = signals[:5]

# one cycle is half a month

year = Voice(1, rate=1/24, chord=(C1, DOM))
year.set([1, 0])
# year.mute(True)

month = Voice(2, rate=0.5, chord=(C2, DOM))
month.set([1, 0])
# month.mute(True)

days = Voice(10, rate=1, chord=None)    # more like half a week
days.set([b(54), p(54), b(54), p(54)] * 2)
# days.mute(True)


patterns = [    [b(1), p(1), b(1), p(1)] * 2,
                [b(2), b(2), p(2), p(2)] * 2,
                [b(3), [p(3), p(3)], b(3), [p(3), p(3)]] * 2,
                [b(4), p(4), b(4), p(4)] * 2,
                [b(5), b(5), 0, p(5)] * 2,  
                ]

for s, signal in enumerate(signals):
    f = signal_from_timeseries(signal)
    plot(f, color="red")
    channel = s + 3 if s < 8 else s + 4
    v = Voice(channel, rate=1, chord=(C, LYD), controls={'volume': 2})
    v.set(patterns[s % len(patterns)])
    v.velocity.set(0.0)
    v.velocity.tween(1.0, 24, f, repeat=True, flip=False)
    v.volume.tween(127, 24, f, repeat=True, flip=False)

    
show_plots()
play()

