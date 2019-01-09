import random

import networkx
import numpy


def remove_nodes_random_uniform():
    random_int = random.randint(0, G.number_of_nodes() - 1)
    nodes = G.nodes()
    G.remove_node(nodes[random_int])


def remove_edges_random_uniform():
    random_list = list(numpy.random.randint(2, size=G.number_of_edges()))
    placement = 0
    for i in range(len(random_list)):
        edges = list(G.edges())
        if random_list[i] == 1:
            G.remove_edge(edges[i - placement][0], edges[i - placement][1])
            placement += 1


def add_edges_random_uniform():
    random_list = numpy.random.rand(G.number_of_nodes(), G.number_of_nodes())
    i = 0
    for row in random_list:
        row_list = list(row)
        for j in range(len(row_list)):
            if row[j] > 0.5:
                G.add_edge(list(G.nodes)[i], list(G.nodes)[j])
        i += 1


def add_nodes_random_uniform():
    nodes_to_add = random.randint(1000)
    for i in range(nodes_to_add):
        node_number = max(list(G.nodes())) + i
        G.add_node(node_number)
        random_list = list(numpy.random.randint(2, size=G.number_of_nodes()))

        for j in range(len(random_list)):
            if random_list[j] == 1:
                G.add_edge(node_number, list(G.nodes())[j])

        random_list = list(numpy.random.randint(2, size=G.number_of_nodes()))
        for j in range(len(random_list)):
            if random_list[j] == 1:
                G.add_edge(list(G.nodes())[j], node_number)


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

pr = networkx.pagerank(G, alpha=0.85)
maximum = max(list(pr.values()))
minimum = min(list(pr.values()))
average = numpy.mean(list(pr.values()))
std = numpy.std(list(pr.values()))
print("minimum: " + str(minimum))
print("maximum: " + str(maximum))
print("average: " + str(average))
print("Standard Deviation Page Rank: " + str(std))

# remove_nodes_random_uniform()
# remove_edges_random_uniform()
add_edges_random_uniform()


pr = networkx.pagerank(G, alpha=0.85)
maximum = max(list(pr.values()))
minimum = min(list(pr.values()))
average = numpy.mean(list(pr.values()))
std = numpy.std(list(pr.values()))
print("minimum: " + str(minimum))
print("maximum: " + str(maximum))
print("average: " + str(average))
print("Standard Deviation Page Rank: " + str(std))

# counter = 1
# description = ""
# for key, value in pr.items():
#     if counter % 3 == 0:
#         description += str(key) + " & " + str(value)
#         description += "\\\\ \hline"
#         print(description)
#         description = ""
#     else:
#         description += str(key) + " & " + str(value) + " & "
#     counter += 1

# print(pr)