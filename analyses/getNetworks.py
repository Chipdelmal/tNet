#!/usr/bin/python
# -*- coding: utf-8 -*-

import osmnx as ox
import style as sty
import pandas as pd
import pickle as pkl
import networkx as nx
import functions as fun

###############################################################################
# Setup and check OSMNX
###############################################################################
ox.config(log_console=True, use_cache=True)
ox.__version__

(PLACE, netType, EXPORT) = (
        'Berkeley, California, USA', 'all', True
    )
idStr = ''.join([i[:3].strip() for i in PLACE.split(',')])
###############################################################################
# Get Network and Projections
###############################################################################
G = ox.graph_from_place(PLACE, netType)
G = ox.project_graph(G)
gdf = ox.gdf_from_place(PLACE)
area = ox.project_gdf(gdf).unary_union.area
if EXPORT:
    file = open('./dta/{}-{}-G.pickle'.format(idStr, netType), 'wb')
    pkl.dump(G, file)
    file.close()

###############################################################################
# Plot the original network
###############################################################################
(fig, ax) = ox.plot_graph(
        G,
        bgcolor=sty.BKG,
        node_size=sty.NS, node_color=sty.NC, node_zorder=sty.NZ,
        edge_linewidth=sty.ES, edge_color=sty.EC, edge_alpha=sty.EA
    )
if EXPORT:
    fig.savefig(
            './img/{}-{}-O.pdf'.format(idStr, netType),
            bbox_inches='tight', pad_inches=.01
        )

###############################################################################
# Closeness Centrality
###############################################################################
node_centrality = nx.closeness_centrality(G)
df = pd.DataFrame(
        data=pd.Series(node_centrality).sort_values(),
        columns=['cc']
    )

###############################################################################
# Plot the network with metrics
###############################################################################
df['colors'] = ox.get_colors(n=len(df), cmap='bwr', start=0.2)
df = df.reindex(G.nodes())
nc = df['colors'].tolist()
(fig, ax) = ox.plot_graph(
        G,
        bgcolor=sty.BKG,
        node_size=sty.NS*2, node_color=nc, node_zorder=sty.NZ,
        edge_linewidth=sty.ES/2, edge_color=sty.EC, edge_alpha=sty.EA
    )
if EXPORT:
    fig.savefig(
            './img/{}-{}-C.pdf'.format(idStr, netType),
            bbox_inches='tight', pad_inches=.01
        )

###############################################################################
# Network stats
###############################################################################
stats = ox.basic_stats(G, area=area)
extended_stats = ox.extended_stats(G, ecc=True, bc=True, cc=True)
for key, value in extended_stats.items():
    stats[key] = value

if EXPORT:
    pd.Series(stats).to_csv('./dta/{}-{}-S.csv'.format(idStr, netType))
    file = open('./dta/{}-{}-S.pickle'.format(idStr, netType), 'wb')
    pkl.dump(stats, file)
    file.close()

###############################################################################
# Betwenness Centrality
###############################################################################
nc = fun.get_node_colors_by_stat(
        G, data=extended_stats['betweenness_centrality']
    )
(fig, ax) = ox.plot_graph(
        G,
        bgcolor=sty.BKG,
        node_size=sty.NS*2, node_color=nc, node_zorder=sty.NZ,
        edge_linewidth=sty.ES/2, edge_color=sty.EC, edge_alpha=sty.EA
    )
if EXPORT:
    fig.savefig(
            './img/{}-{}-B.pdf'.format(idStr, netType),
            bbox_inches='tight', pad_inches=.01
        )
