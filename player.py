#!/usr/bin/env python3

from main import signals
from braid import *

core.log_midi = True
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

signals = signals[0:5]

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

# def check(n):
#     def f(v):
#         return n
#         if v.volume() > 0 and v.playing() == 0:
#             v.playing(1)
#             print('START', v.volume())
#             return n
#         elif v.volume() == 0 and v.playing() == 1:
#             v.playing(0)
#             print('STOP')
#             return n
#         else:
#             return n
#     return f

channels = [2, 3, 4, 5, 6, 7]     # why does the first one not play?
notes = [1, 2, 3, 4, 5, 6]
for s, signal in enumerate(signals):
    if s == len(channels):
        break
    f = signal_from_timeseries(signal)
    plot(f, color="red")
    print('channel', channels[s])
    v = Voice(channels[s], rate=1, chord=(C, LYD), controls={'volume': 7})
    # v.set(patterns[s % len(patterns)])
    v.set([s])
    # v.velocity.set(0.0)
    # v.velocity.tween(1.0, 24, f, repeat=True, flip=False)
    v.volume(10)
    v.volume.tween(127, 24, f, repeat=True, flip=False)
    v.add("playing")

    
show_plots()
play()

