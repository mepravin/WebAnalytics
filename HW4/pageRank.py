import random

import networkx
import numpy


# remove node with certain strategy
def remove_node(method="random", page_rank=None, maximum=True):
    global G
    # get a node uniform at random
    node_number = -1
    if method == "random":
        random_number = random.randint(0, G.number_of_nodes() - 1)
        node_number = list(G.nodes())[random_number]
    # get the node with the highest/lowest degree
    elif method == "degree":
        max_degree = 0
        min_degree = G.number_of_edges() + 1
        # for each node, check whether the degree is maximum/minimum degree
        # if node has maximum/minimum degree, save the degree and the node
        for node in list(G.nodes()):
            # if we want the maximum degree
            if maximum:
                if G.degree(node) >= max_degree:
                    node_number = node
                    max_degree = G.degree(node)
            # else the minimum degree
            else:
                if G.degree(node) <= min_degree :
                    node_number = node
                    min_degree = G.degree(node)
    # get the node with the highest/lowest page rank
    elif method == "page_rank":
        max_page_rank = 0
        min_page_rank = 1.0
        # for each node, check whether the page_rank is maximum/minimum page_rank
        # if node has maximum/minimum page rank, save the page rank and the node
        for node in list(G.nodes()):
            # if we want the maximum page rank
            if maximum:
                if page_rank[node] >= max_page_rank:
                    node_number = node
                    max_page_rank = page_rank[node]
            # else we want the minimum page rank
            else:
                if page_rank[node] <= min_page_rank:
                    node_number = node
                    min_page_rank = page_rank[node]

    # remove the node found before
    G.remove_node(node_number)


# remove edge with certain strategy
def remove_edge(method="random", page_rank=None, maximum=True):
    # get a random a random edge
    if method == "random":
        edge = random.randint(0, G.number_of_edges() - 1)
        edge = list(G.edges())[edge]
    else:
        node_number = -1
        # get the node with the highest/lowest degree, and remove a edge adjacent to this node
        if method == "degree":
            max_degree = 0
            min_degree = G.number_of_edges() + 1
            # for each node, check whether the degree is maximum/minimum degree
            # if node has maximum/minimum degree, save the degree and the node
            for node in list(G.nodes()):
                # we only want a node with adjacent edges to be able to remove an adjacent edge
                if G.degree(node) < 1:
                    continue
                # if we want the maximum degree
                if maximum:
                    if G.degree(node) >= max_degree:
                        node_number = node
                        max_degree = G.degree(node)
                # else we want the minimum degree
                else:
                    if G.degree(node) <= min_degree and G.degree(node) > 1:
                        node_number = node
                        min_degree = G.degree(node)
        # get the node with the highest/lowest page rank, and remove a edge adjacent to this node
        elif method == "page_rank":
            max_page_rank = 0
            min_page_rank = 1.0
            # for each node, check whether the page_rank is maximum/minimum page_rank
            # if node has maximum/minimum page rank, save the page rank and the node
            for node in list(G.nodes()):
                # we only want a node with adjacent edges to be able to remove an adjacent edge
                if G.degree(node) < 1:
                    continue

                # if we want the highest page rank
                if maximum:
                    if page_rank[node] >= max_page_rank:
                        node_number = node
                        max_page_rank = page_rank[node]
                # else we want the lowest page rank
                else:
                    if min_page_rank >= page_rank[node] > 0:
                        node_number = node
                        min_page_rank = page_rank[node]

        # take a random edge adjacent to this node
        edges = list(G.edges(node_number))
        edge = edges[random.randint(0, len(edges) - 1)]

    # get the nodes of the edge
    from_node = edge[0]
    to_node = edge[1]
    # remove the edge
    G.remove_edge(from_node, to_node)


# add a edge according to a certain strategy
def add_edge(method="random", page_rank=None, maximum=True):
    # add a edge between two random nodes
    if method == "random":
        from_node = random.randint(0, G.number_of_nodes() - 1)
        to_node = random.randint(0, G.number_of_nodes() - 1)
    # find a specific node to add edge to
    else:
        # decide whether the node is the from node or to node
        # if it is true, it is the node the edge comes from
        from_node_bool = bool(random.getrandbits(1))
        node_number = -1
        #get the node with the highest/lowest degree
        if method == "degree":
            max_degree = 0
            min_degree = G.number_of_edges() + 1
            # for each node, check whether the degree is maximum/minimum degree
            # if node has maximum/minimum degree, save the degree and the node
            for node in list(G.nodes()):
                # if we want the highest degree
                if maximum:
                    if G.degree(node) >= max_degree:
                        node_number = node
                        max_degree = G.degree(node)
                # if we want the lowest degree
                else:
                    if G.degree(node) <= min_degree:
                        node_number = node
                        min_degree = G.degree(node)
        # get the node with the highest/lowest page rank, and add a edge adjacent to this node
        elif method == "page_rank":
            max_page_rank = 0
            min_page_rank = 1.0
            # for each node, check whether the page_rank is maximum/minimum page_rank
            # if node has maximum/minimum page rank, save the page rank and the node
            for node in list(G.nodes()):

                if node not in page_rank:
                    continue

                # if we want the highest page rank
                if maximum:
                    if page_rank[node] >= max_page_rank:
                        node_number = node
                        max_page_rank = page_rank[node]
                # if we want the lowest page rank
                else:
                    if page_rank[node] <= min_page_rank:
                        node_number = node
                        min_page_rank = page_rank[node]
        # set the from_node and to_node according to the from_node_bool
        if from_node_bool:
            from_node = node_number
            to_node = random.randint(0, G.number_of_nodes() - 1)
        else:
            from_node = random.randint(0, G.number_of_nodes() - 1)
            to_node = node_number

    #Add the edge to the graph
    G.add_edge(from_node, to_node)


# add nodes random (we did not define a strategy, since all strategies are based upon statistics of a node)
def add_nodes_random():
    # find largest number and add one, this will be the new node
    node_number = max(list(G.nodes())) + 1
    # add the node to the graph
    G.add_node(node_number)
    # randomly define how much edges are added (range 0-100%)
    percentage = random.uniform(0, 10)
    # create two random lists, for each node we assign a value between 0 and 10
    random_list_to = list(numpy.random.uniform(10, size=G.number_of_nodes()))
    random_list_from = list(numpy.random.uniform(10, size=G.number_of_nodes()))
    for j in range(len(random_list_from)):
        # if the assigned value is larger than the percentage a edge will be added from this node to the new node
        if random_list_from[j] > percentage:
            G.add_edge(list(G.nodes())[j], node_number)

        # if the assigned value is larger than the percentage a edge will be added from the new node to this node
        if random_list_to[j] > percentage:
            G.add_edge(node_number, list(G.nodes())[j])


# add the page rank from the new node to the baseline. We add the average value for a node.
def add_page_rank(page_rank_start):
    #assign the average page rank to the new node
    page_rank_start[max(list(G.nodes()))] = 1 / G.number_of_nodes()
    #create the sorted ranking baseline
    page_rank_baseline = [k for k in sorted(page_rank, key=page_rank.get, reverse=True)]
    page_rank_baseline_category = dict()
    counter = 1
    for item in page_rank_baseline:
        page_rank_baseline_category[item] = counter
        counter += 1
    #return the new page rank, and the rank baseline
    return page_rank_start, page_rank_baseline_category


# print the page rank
def print_page_rank(pr):
    for key, value in pr.items():
        description = str(key) + " " + str(value)
        print(description)


# evolve the graph and report the error rank and degree rank
# we will take 20 steps of 200 removals, for each time step the error rank and degree rank is saved
# if we have a method which relies on randomness, we do this process 10 times and in the end we take the average for
# each time step.
# if the method is not based on randomness, it suffices to do the process only once (since all iterations will return
# the same result
def evolving_graph():
    global G
    # create a list of lists for the error ranks and degree ranks
    error_ranks = [[] for _ in range(20)]
    error_values = [[] for _ in range(20)]
    # save the original G as start_G
    start_G = G.copy()
    for _ in range(10):
        # at the start of each iteration, start with original G
        G = start_G.copy()
        # create the base line page rank
        page_rank = networkx.pagerank(G, alpha=0.85)
        page_rank_baseline = page_rank
        # sort the page ranks to create the ranks baseline
        page_rank_sorted = [k for k in sorted(page_rank, key=page_rank.get, reverse=True)]
        rank_baseline = dict()
        # go through each item in the sorted page rank and save the rank in the dictionary rank_baseline
        counter = 1
        for item in page_rank_sorted:
            rank_baseline[item] = counter
            counter += 1

        # we have 20 time steps in which we remove 200 edges/nodes
        for t in range(20):
            # get the right list for the error rank and degree rank
            error_rank_t = error_ranks[t]
            error_value_t = error_values[t]
            # apply the action and method
            for i in range(200):
                # change these lines to do other action or method
                # define the method (random, degree or page_rank)
                method = "page_rank"
                add_nodes_random()

            # calculate the new page rank
            page_rank = networkx.pagerank(G, alpha=0.85)

            # sort the new page rank
            page_rank_sort = [k for k in sorted(page_rank, key=page_rank.get, reverse=True)]

            # go through each item in the sorted page rank and save the rank in the dictionary rank_baseline
            page_rank_sort_category = dict()
            counter = 1
            for item in page_rank_sort:
                page_rank_sort_category[item] = counter
                counter += 1

            # calculate the error rank and error value as given in the homework assignment
            error_rank = 0
            error_value = 0
            for key, value in rank_baseline.items():
                # check whether the key still exists, it could be removed due to the method remove edge
                if key in page_rank_sort_category:
                    page_i_rank = page_rank_sort_category[key]

                    error_rank += abs(page_i_rank - value) / value

                # check whether the key still exists, it could be removed due to the method remove edge
                if key in page_rank:
                    page_i = page_rank[key]
                    base_line = page_rank_baseline[key]
                    error_value += abs(page_i - base_line) / value

            error_rank_t.append(error_rank)
            error_value_t.append(error_value)

    # print the average of the error_ranks and error_values at each time step
    for error_rank_t in error_ranks:
        print(numpy.mean(error_rank_t))

    for error_value_t in error_values:
        print(numpy.mean(error_value_t))


# create the graph and read in the data
G = networkx.Graph()
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


#start evolving the graph
evolving_graph()



# pr = networkx.pagerank(G, alpha=0.85)
# maximum = max(list(pr.values()))
# minimum = min(list(pr.values()))
# average = numpy.mean(list(pr.values()))
# std = numpy.std(list(pr.values()))
# print("minimum: " + str(minimum))
# print("maximum: " + str(maximum))
# print("average: " + str(average))
# print("Standard Deviation Page Rank: " + str(std))

