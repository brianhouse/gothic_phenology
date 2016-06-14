#!/usr/bin/env python3

from phenology import signals, onsets, peaks
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

signals = signals[0:8]

# one cycle is half a month

# year = Voice(1, rate=1/24, chord=(C1, DOM), controls={'volume': 127})
# year.set([1, 0])
# year.mute(True)

# month = Voice(2, rate=0.5, chord=(C2, DOM), controls={'volume': 127})
# month.set([1, 0])
# month.mute(True)

# days = Voice(10, rate=1, chord=None, controls={'volume': 127})
# days.set([b(54), p(54), b(54), p(54)] * 2)
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

channels = [1, 2, 3, 4, 5, 6, 7, 8]
notes =    [1, 2, 3, 4, 5, 6, 7, 8]
for s, signal in enumerate(signals):
    if s == len(channels):
        break
    print("channel", channels[s])
    f = signal_from_timeseries(signal)
    plot(f, color="red")
    v = Voice(channels[s], rate=1, chord=(C4, LYD), controls={'volume': 20})
    # v.volume(10)
    # v.volume.tween(127, 24, f, repeat=True, flip=False)
    # v.set([0])
    v.set([notes[s]] * 4)    
    # v.play(notes[s])

    # # one year is 24 cycles
    # # one cycle is driver.rate    
    # for onset in onsets[s]:
    #     v.play_at((onset / len(signal)) * (driver.rate * 24) - 1.0, 0, 1.0)                
    #     v.play_at((onset / len(signal)) * (driver.rate * 24), notes[s], 1.0)
    # for peak in peaks[s]:
    #     v.play_at((peak / len(signal)) * (driver.rate * 24) - 1.0, 0, 1.0)        
    #     v.play_at((peak / len(signal)) * (driver.rate * 24), notes[s], 1.0)

    
show_plots()
play()

