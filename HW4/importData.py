import random

import networkx
import numpy

G = networkx.DiGraph()
edges = set()
with open('out.advogato', 'r') as ins:
    for line in ins:
        if '%' in line:
            continue
        else:
            line.rstrip()
            array = line.split()
            from_node = int(array[0])
            to_node = int(array[1])
            G.add_node(from_node)
            G.add_node(to_node)
            G.add_edge(from_node, to_node)

print(G)