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

NORMALIZE = True
TAIL = 172800 # 2 days

species_list = []
species_list = ['Taraxacum officinale', 'Collomia linearis', 'Hydrophyllum fendleri']
# species_list = ['Collomia linearis']
# species_list = ['Carex nigricans']


# load data into t and count arrays per species
species = {}
start_t = util.timestamp(util.parse_date(START))
end_t = util.timestamp(util.parse_date(END))
max_count = 0
with open("data.csv") as f:
    data = csv.reader(f)
    for r, row in enumerate(data):
        if r == 0:
            continue
        plot = row[1]        
        name = row[2]        
        if len(species_list) and name not in species_list:
            continue
        dt = datetime.datetime(int(row[3]), 1, 1) + datetime.timedelta(int(row[4]) - 1)
        t = util.timestamp(dt)
        if t < start_t or t > end_t:
            continue
        count = 0 if row[5] == "NA" else int(row[5]) 
        if count > max_count:
            max_count = count
        if name not in species:
            species[name] = {'ts': [start_t, t - 1], 'counts': [0, 0]}
        species[name]['ts'].append(t)
        species[name]['counts'].append(count)
print("--> loaded")


# add a zero count at the start and end of every year
yts = [util.timestamp(datetime.datetime(y, 1, 1)) for y in range(1974, 2017)]
for s in species:
    ts = species[s]['ts']
    for yt in yts:
        i = 0        
        while i < len(ts) and ts[i] < yt:
            i += 1
        if i > 0:
            end_season_t = ts[i-1]
            if i < len(ts):
                start_season_t = ts[i]
                ts.insert(i, start_season_t - TAIL)
                species[s]['counts'].insert(i, 0)
            ts.insert(i, end_season_t + TAIL)
            species[s]['counts'].insert(i, 0)                            
    species[s]['ts'].append(end_t)
    species[s]['counts'].append(0)
print("--> onsets added")


# create and draw signals
ctx = drawing.Context(1500, 500)
i = 0
for name, s in species.items():
    print("Drawing %s..." % name)
    color = random(), random(), random(), 1.
    signal = sp.resample(s['ts'], s['counts'])
    if NORMALIZE:
        signal = sp.normalize(signal)
    else:
        signal = sp.normalize(signal, 0, max_count)    
    signal = sp.smooth(signal, size=8)
    ctx.plot(signal, stroke=color, thickness=2)
    ctx.line(10 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), 30 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), stroke=color, thickness=2)
    # ctx.label(0.5, 0.5, "test")
    i += 1

ctx.output("charts")

