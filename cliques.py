#!/usr/bin/python3

import networkx as nx
import time
import itertools

def BuildNetworkxGraphFromFile(file_name):
    import re # regular expressions
    G1 = nx.Graph() # undirected graph
    lines = [line.strip() for line in open(file_name)]
    for line in lines:
        l = re.split('\t| ',line)
        G1.add_edge(int(l[0]),int(l[1]))
    return G1

def find_cliques(ifile, ofile, mode='Iterative', verbose=False):
    G = BuildNetworkxGraphFromFile(ifile)
    start = time.time()
    if mode == "Iterative":
        gen_a, gen_b = itertools.tee(nx.find_cliques(G))
    else:
        gen_a, gen_b = itertools.tee(nx.find_cliques_recursive(G))

    clique_count = 0

    for clique in gen_a:
        clique_count += 1

    end = time.time()

    if ofile != None:
        f = open(ofile, 'w')
        for clique in gen_b:
            f.write("%s\n" % clique)
    else:
        for clique in gen_b:
            clique_count += 1
            print(clique)

    if verbose:
        print("\tTime to enumerate {0} cliques: \033[1m{1:.2f}\033[0m".format(clique_count,end-start))