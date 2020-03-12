
import osmnx as ox
import pandas as pd
import networkx as nx
# import matplotlib.cm as cm
# import matplotlib.colors as colors

###############################################################################
# Setup and check OSMNX
###############################################################################
ox.config(log_console=True, use_cache=True)
ox.__version__

(place, netType) = ('Emeryville, California, USA', 'drive_service')
idStr = [i[:3].strip() for i in place.split(',')]
###############################################################################
# Get Network and Projections
###############################################################################
G = ox.graph_from_place(place, netType)
G = ox.project_graph(G)
gdf = ox.gdf_from_place(place)
area = ox.project_gdf(gdf).unary_union.area

###############################################################################
# Plot the original network
###############################################################################
(fig, ax) = ox.plot_graph(
        G,
        bgcolor='k', node_size=30, node_color='#999999',
        node_edgecolor='none', node_zorder=2,
        edge_color='#555555', edge_linewidth=1.5, edge_alpha=1
    )

###############################################################################
# Get metrics
###############################################################################
node_centrality = nx.closeness_centrality(G)
df = pd.DataFrame(
        data=pd.Series(node_centrality).sort_values(),
        columns=['cc']
    )
df['colors'] = ox.get_colors(
        n=len(df), cmap='inferno', start=0.2
    )
df = df.reindex(G.nodes())
nc = df['colors'].tolist()

###############################################################################
# Plot the network with metrics
###############################################################################
(fig, ax) = ox.plot_graph(
        G,
        bgcolor='k', node_size=30, node_color=nc, node_edgecolor='none',
        node_zorder=2, edge_color='#555555', edge_linewidth=1.5, edge_alpha=.75
    )

###############################################################################
# Network stats
###############################################################################
stats = ox.basic_stats(G, area=area)
extended_stats = ox.extended_stats(G, ecc=True, bc=True, cc=True)
for key, value in extended_stats.items():
    stats[key] = value
pd.Series(stats)
