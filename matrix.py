import time
import numpy as np
from scipy.sparse import csr_matrix

def createVertexCommunityMatrix(filename, vc_weight_method='edges', diagonal_value=1, neighbor_value=1, d_weight_method='edges',
                                verbose=False):
    start = time.time()
    num_of_communities, num_of_vertexes = findMatrixShape(filename)
    end = time.time()
    if verbose:
        print("\t\tTime to find the shape: \033[1m{0:.2f} s\033[0m".format(end-start))
    
    vc = np.zeros((num_of_vertexes,num_of_communities))
    d = np.zeros((num_of_vertexes,num_of_vertexes))
    vertex_set = [i+1 for i in range(num_of_vertexes)]
    
    start = time.time()
    with open(filename) as file:
        c = 0
        for line in file:
            vertexes = lineParser(line)
            comm_size = len(vertexes)
            comm_weight = weightCommunity(vc_weight_method, comm_size)
            for i in range(len(vertexes)):
                v = vertexes[i]
                d[v-1,v-1] += diagonal_value * weightCommunity(d_weight_method, comm_size)
                vc[v-1,c] = comm_weight
                for j in range(i+1,len(vertexes)):
                    n = vertexes[j]
                    d[v-1,n-1] += neighbor_value * weightCommunity(d_weight_method, comm_size)  
                    d[n-1,v-1] += neighbor_value * weightCommunity(d_weight_method, comm_size)  
            c += 1
    end = time.time()
    if verbose:
        print("\t\tTime to create and weight dict: \033[1m{0:.2f} s\033[0m".format(end-start))

    start_t2 = time.time()
    d = csr_matrix(d)
    vc = csr_matrix(vc)
    end_t2 = time.time()
    if verbose:
        print("\t\tTime to create sparse matrices from dict: \033[1m{0:.2f} s\033[0m".format(end_t2-start_t2))
    return (num_of_communities,num_of_vertexes,vc,d,vertex_set)

def weightCommunity(method, size):
    if method == 'edges':
        return (size * (size - 1) / 2)
    if method == 'dim':
        return (size)
    if method == 'one':
        return (1)
    
# function to find the shape of the vertex-community matrix (that is the number of vertexes and communities)
def findMatrixShape(filename):
    with open(filename) as file:
        num_of_communities = 0
        vertexes = set()
        for line in file:
            num_of_communities += 1
            vertexes.update(list(map(int,line[1:-2].split(", "))))
    return (num_of_communities,len(vertexes))
    
# this function removes brackets, and returns a list of int using the string ", " as separator
def lineParser(line):
    return list(map(int,line[1:-2].split(", ")))