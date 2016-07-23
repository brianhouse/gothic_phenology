#!/usr/bin/env python3

import csv, datetime
import signal_processing as sp
import numpy as np
from random import random
from housepy import util, drawing, strings
from collections import OrderedDict
from colors import colors

# START = "1973-01-01"
START = "2014-01-01"
# START = "2010-01-01"
# END = "1973-12-31"
END = "2015-12-31"

NORMALIZE = True
TAIL = 172800 # 2 days

species_list = []
# species_list = ['Taraxacum officinale', 'Collomia linearis', 'Hydrophyllum fendleri']
# species_list = ['Festuca thurberi', 'Elymus glaucus', 'Salix sp.', 'Stellaria longifolia', 'Erigeron coulteri', 'Hydrophyllum capitatum', 'Ranunculus inamoenus', 'Epilobium brachycarpum', 'Erigeron elatior', 'Oxypolis fendleri']
# species_list = ['Collomia linearis']
# species_list = ['Carex nigricans']
species_list = ["Claytonia lanceolata", "Mertensia fusiformis", "Hydrophyllum capitatum", "Erythronium grandiflorum", "Delphinium nuttallianum", "Adenolinum lewisii", "Erigeron flagellaris", "Delphinium barbeyi", "Dugaldia hoopesii", "Erigeron speciosus", "Heterotheca villosa"]


def generate(onset_spikes=False, peak_spikes=False):

    # load data into t and count arrays per species
    species = OrderedDict()
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
                    ts.insert(i, start_season_t - TAIL)
                    species[name]['counts'].insert(i, 0)
                ts.insert(i, end_season_t + TAIL)
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
        if NORMALIZE:
            signal = sp.normalize(signal)
        else:
            signal = sp.normalize(signal, 0, max_count)    
        signal = sp.smooth(signal, size=8)
        signal = sp.limit(signal, max(signal))  # get rid of noise below 0 for onset detection

        # add spikes for peaks
        if peak_spikes:
            peaks, valleys = sp.detect_peaks(signal, lookahead=50)
            peak_signal = np.zeros(len(signal))    
            for peak in peaks:
                peak_signal[peak[0]] = 1.0
            signal += peak_signal

        # add spikes for onsets
        if onset_spikes:
            onsets = sp.detect_onsets(signal)
            onset_signal = np.zeros(len(signal))    
            for onset in onsets:
                onset_signal[onset] = 0.5
            signal += onset_signal

        # limit
        signal = sp.limit(signal, 1.0)
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