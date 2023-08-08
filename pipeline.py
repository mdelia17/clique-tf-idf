from cliques import find_cliques
from matrix import createVertexCommunityMatrix
from clustering import bestModelBinarySearch

import argparse
import time
import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
from sklearn.metrics import pairwise_distances
import warnings

def createGraph(filename):
    G = nx.Graph()
    with open(filename) as file:
        for line in file:
            edges = line.strip().split(" ")
            G.add_edge(int(edges[0]),int(edges[1]))
    return G

parser = argparse.ArgumentParser(description='Clique-TF-IDF')
parser.add_argument('--file', '-f',
                    help='Full path to the file where the graph is located.',
                    required=True)
parser.add_argument('--verbose', '-v',
                    dest='verbose',
                    default=False,
                    help='Produce verbose output',
                    action='store_true')
parser.add_argument('--output', '-o',
                    help='Name of output file for clusters')

args = parser.parse_args()
ifile = args.file
comms_file = args.file.replace('edges','comms')
verbose = args.verbose
ofile = args.output

warnings.simplefilter(action='ignore', category=FutureWarning)

tfidf_model = TfidfTransformer(norm=None)

find_cliques(ifile, comms_file, verbose=verbose)

G = createGraph(ifile)

start_t1 = time.time()
num_of_communities,num_of_vertexes,vc,d,vertex_set = createVertexCommunityMatrix(
    comms_file, vc_weight_method='one', diagonal_value=1, neighbor_value=1, d_weight_method='edges', verbose=verbose)
end_t1 = time.time()
if verbose:
    print("\tSize of the problem (NxMxC): \033[1m{} x {} x {}\033[0m".format(num_of_vertexes,len(G.edges()),num_of_communities))
    print("\tTime to create X and Y: \033[1m{0:.2f} s\033[0m".format(end_t1-start_t1))

start_t2 = time.time()
Z = d.dot(vc)
end_t2 = time.time()
if verbose:
    print("\tTime to create Z: \033[1m{0:.2f} s\033[0m".format(end_t2-start_t2))

start_t3 = time.time()
Z_transformed = tfidf_model.fit_transform(Z)
Z_transformed = normalize(Z_transformed,norm='max',axis=0) # column min-max normalization
Z_transformed = normalize(Z_transformed,norm='l2',axis=1) # vector normalization without TF-IDF
end_t3 = time.time()
if verbose:
    print("\tTime to transform Z: \033[1m{0:.2f} s\033[0m".format(end_t3-start_t3))

# VC distance matrix with scikit
start_t5 = time.time()
D = pairwise_distances(Z_transformed, metric='euclidean', n_jobs=None)
end_t5 = time.time()
if verbose:
    print('\tTime to find distance matrix: \033[1m{0:.2f} s\033[0m'.format(end_t5-start_t5))

start_t6 = time.time()
best_k, best_clustering_labels, best_modularity = bestModelBinarySearch(
    D, G, (1,D.shape[0]//2), vertex_set, resolution=1, verbose=False)
end_t6 = time.time()
if verbose:
    print('\tTime to find best clustering: \033[1m{0:.2f} s\033[0m'.format(end_t6-start_t6))

t_total = (end_t1-start_t1) + (end_t2-start_t2) + (end_t3-start_t3) + (end_t5-start_t5) + (end_t6-start_t6)
if verbose:
    print("Time to cluster the graph with Clique-TF-IDF: \033[1m{0:.2f} s\033[0m".format(t_total))
    print("Modularity of the clustering: \033[1m{0:.4f} \033[0m".format(best_modularity))

if ofile != None:
    i = 1
    with open(ofile, 'w') as file:
        for label in best_clustering_labels:
            file.write('{} {}\n'.format(i,label))
            i += 1
else:
    print(best_clustering_labels)