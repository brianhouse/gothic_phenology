#!/usr/bin/env python3

import csv, datetime
import signal_processing as sp
from random import random
from housepy import util, drawing

# START = "1973-01-01"
# START = "2015-01-01"
START = "2010-01-01"
# END = "1973-12-31"
END = "2015-12-31"


species = {}
start_t = util.timestamp(util.parse_date(START))
end_t = util.timestamp(util.parse_date(END))

with open("data.csv") as f:
    data = csv.reader(f)
    for r, row in enumerate(data):
        if r == 0:
            continue
        plot = row[1]        
        name = row[2]        
        dt = datetime.datetime(int(row[3]), 1, 1) + datetime.timedelta(int(row[4]) - 1)
        t = util.timestamp(dt)
        if t < start_t or t > end_t:
            continue
        count = 0 if row[5] == "NA" else int(row[5]) 
        if name not in species:
            species[name] = {'ts': [start_t, t - 1], 'counts': [0, 0]}
        species[name]['ts'].append(t)
        species[name]['counts'].append(count)

for s in species:
    species[s]['ts'].append(species[s]['ts'][-1] + 1)
    species[s]['ts'].append(end_t)
    species[s]['counts'].append(0)
    species[s]['counts'].append(0)


ctx = drawing.Context(1000, 200)

species_list = ['Taraxacum officinale', 'Collomia linearis', 'Hydrophyllum fendleri']

for s in species_list:
    if s not in species:
        continue
    color = random(), random(), random(), 1.
    print(s, color)
    s = species[s]
    signal = sp.resample(s['ts'], s['counts'])
    signal = sp.normalize(signal)
    signal = sp.smooth(signal, size=8)
    ctx.plot(signal, stroke=color, thickness=2.)

ctx.output("charts")

