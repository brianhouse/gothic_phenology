#!/usr/bin/env python3

import csv, datetime
import signal_processing as sp
import numpy as np
from random import random
from housepy import util, drawing, strings, config
from collections import OrderedDict
from colors import colors

def generate():

    # load data into t and count arrays per species
    species = OrderedDict()
    start_t = util.timestamp(util.parse_date(str(config['start'])))
    end_t = util.timestamp(util.parse_date(str(config['end'])))
    max_count = 0
    with open("data.csv") as f:
        data = csv.reader(f)
        for r, row in enumerate(data):
            if r == 0:
                continue
            plot = row[1]        
            name = row[2]        
            if len(config['species_list']) and name not in config['species_list']:
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
    species = OrderedDict(sorted(species.items()))
    print("--> loaded")


    # add a zero count at the start and end of every year
    yts = [util.timestamp(datetime.datetime(y, 1, 1)) for y in range(1974, 2017)]
    for name in species:
        ts = species[name]['ts']
        for yt in yts:
            i = 0        
            while i < len(ts) and ts[i] < yt:
                i += 1
            if i > 0:
                end_season_t = ts[i-1]
                if i < len(ts):
                    start_season_t = ts[i]
                    ts.insert(i, start_season_t - config['tail'])
                    species[name]['counts'].insert(i, 0)
                ts.insert(i, end_season_t + config['tail'])
                species[name]['counts'].insert(i, 0)
        species[name]['ts'].append(end_t)
        species[name]['counts'].append(0)
    print("--> onsets added")


    # create and draw signals
    signals = []
    names = []
    i = 0
    for name, data in species.items():
        print("Processing %s..." % name)

        # create signal from bloom counts
        signal = sp.resample(data['ts'], data['counts'])
        if config['normalize']:
            signal = sp.normalize(signal)
        else:
            signal = sp.normalize(signal, 0, max_count)    
        signal = sp.smooth(signal, size=8)
        signal = sp.limit(signal, max(signal))  # get rid of noise below 0 for onset detection

        # add spikes for peaks
        if config['peak_spikes']:
            peaks, valleys = sp.detect_peaks(signal, lookahead=50)
            peak_signal = np.zeros(len(signal))    
            for peak in peaks:
                peak_signal[peak[0]] = 1.0
            signal += peak_signal

        # add spikes for onsets
        if config['onset_spikes']:
            onsets = sp.detect_onsets(signal)
            onset_signal = np.zeros(len(signal))    
            for onset in onsets:
                onset_signal[onset] = 0.5
                onset_signal[onset+1] = 0.4
                onset_signal[onset+2] = 0.25
            signal += onset_signal

        # limit
        signal = sp.limit(signal, 1.0)
        signal *= 0.9   # hack, just controlling gain
        signals.append(signal)   

        names.append(name)
   
        i += 1

    return signals, names



if __name__ == "__main__":

    signals, names = generate()
    ctx = drawing.Context(1500, 750)    
    for i, signal in enumerate(signals):
        color = colors[i % len(colors)]        
        ctx.plot(signal, stroke=color, thickness=2)
        ctx.line(10 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), 30 / ctx.width, 1 - ((10 + (i * 10)) / ctx.height), stroke=color, thickness=2)
        ctx.label(35 / ctx.width, 1 - ((13 + (i * 10)) / ctx.height), names[i].upper(), size=10)    
    ctx.output("charts")

    util.save("signals.pkl", signals)