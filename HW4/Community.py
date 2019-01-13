import community
import networkx as nx
import toyplot.data
import numpy as np
import operator
import matplotlib.pyplot as plt


startRank = 0
endRank = 15

# load the edge list and create a directed Graph
# load the edge list
edgelist = []
with open('out.advogato') as f:
	for line in f:
		if not line.startswith('%'):
			nodes = line.split()
			edgelist.append((int(nodes[0]), int(nodes[1])))

# create a Graph using Networkx
# note that we create an undirected graph for simplicity
G = nx.Graph()
G.add_edges_from(edgelist)
#print(edgelist)

partition = community.best_partition(G)
#mod = community.modularity(partition ,G)
#print("modularity:", mod)
#sorted_communities = sorted(partition.items(), key=operator.itemgetter(1), reverse=True)

communities = {}
values = [partition.get(node) for node in G.nodes()]
finalValues = values.copy()
for value in values:
	if value not in communities:
		communities[value] = 1
	else:
		communities[value] += 1

sorted_communities = sorted(communities.items(), key=operator.itemgetter(1), reverse=True)
print("Communities: ", len(sorted_communities))

shortenedCommunities = (sorted_communities.copy())[startRank:endRank]
finalCommunities = []
for community in shortenedCommunities:
	index, amount = community
	finalCommunities.append(index)

nodeIndex = len(values)-1
for node in reversed(values):
	if (node not in finalCommunities):
		if (nodeIndex != 4749 and nodeIndex != 5315 and nodeIndex != 0):
			G.remove_node(nodeIndex)
			finalValues.remove(node)
	nodeIndex -= 1

nx.draw_spring(G, cmap = plt.get_cmap('Set1'), node_color = finalValues, node_size=30, with_labels=False)
plt.show()