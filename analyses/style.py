#!/usr/bin/python
# -*- coding: utf-8 -*-

from matplotlib.colors import LinearSegmentedColormap

BKG = '#000000'
(NS, NC, NZ) = (2, '#f20060B0', 2)
(ES, EC, EA) = (.75, '#89beff', .75)

cdict = {
        'red':   [(0, 0, 0),  (.5, 1, 1),   (1,  1, 1)],
        'green': [(0, 0, 0),  (.5, .5, .5), (1,  0, 0)],
        'blue':  [(0, 1, 1),  (.5, 1, 1),   (1,  0, 0)]
    }
CMAP = LinearSegmentedColormap('WB', cdict, N=256)
