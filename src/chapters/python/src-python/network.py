#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 08:44:50 2020

@author: ah
"""

import matplotlib.pyplot as plt
import networkx as nx
import pygraphviz

import matplotlib.font_manager as font_manager

# Set the font dictionaries (for plot title and axis titles)
title_font = {'fontname':'Arial', 'size':'18', 'color':'black', 'weight':'normal',
  'verticalalignment':'bottom'} # Bottom vertical alignment for more space

try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or pydot")
nodes=3
generation=5
G = nx.balanced_tree(nodes, generation)
pos = graphviz_layout(G, prog='twopi', args='')
plt.figure(figsize=(8, 8))
nx.draw(G, pos, node_size=20, alpha=0.5, node_color="blue", with_labels=False)
plt.title(r'$R_0$='+str(nodes),**title_font)
plt.axis('equal')
plt.savefig('../fig-python/netw_'+str(nodes)+'_'+str(generation)+ '.png', bbox_inches='tight',transparent=True)
plt.show()
print('Number of nodes: ' + str(G.number_of_nodes()))