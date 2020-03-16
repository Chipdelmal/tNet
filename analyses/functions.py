#!/usr/bin/python
# -*- coding: utf-8 -*-

import osmnx as ox
import numpy as np
import pandas as pd
import style as sty
from os import path
import pickle as pkl
import matplotlib.cm as cm


def get_color_list(n, color_map=sty.CMAP, start=0, end=1):
    return [cm.get_cmap(color_map)(x) for x in np.linspace(start, end, n)]


def get_node_colors_by_stat(G, data, start=0, end=1):
    df = pd.DataFrame(data=pd.Series(data).sort_values(), columns=['value'])
    df['colors'] = get_color_list(len(df), start=start, end=end)
    df = df.reindex(G.nodes())
    return df['colors'].tolist()


def loadNetwork(PLACE, netType, ntwPath, write=True):
    if path.exists(ntwPath):
        file = open(ntwPath, 'rb')
        G = pkl.load(file)
        file.close()
    else:
        G = ox.graph_from_place(PLACE, netType)
        if write:
            file = open(ntwPath, 'wb')
            pkl.dump(G, file)
            file.close()
    return G
