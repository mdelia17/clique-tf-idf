from sklearn.cluster import AgglomerativeClustering
import networkx.algorithms.community as nx_comm
import random

def bestModelBinarySearch(data, G, k_interval, vertex_set, resolution=3, verbose=False, **kwargs):
    min_k, max_k = k_interval
    current_k = (min_k + max_k)//2
    best_fit, best_k, best_labels = (-1,0,0)
    yet_trained = {}
    t_effective, t_total = (0,0)

    while ((max_k - min_k) > 2):
        if current_k not in yet_trained:
            t_effective +=1
            t_total +=1
            current_fit, current_labels = train_and_fit(data, G, current_k, vertex_set)
            yet_trained[current_k] = (current_fit,current_labels)
            if current_fit > best_fit:
                best_fit, best_k, best_labels = (current_fit, current_k, current_labels)
        else:
            t_total +=1
            current_fit, current_labels = yet_trained[current_k]
            if current_fit > best_fit:
                best_fit, best_k, best_labels = (current_fit, current_k, current_labels)
        
        where_is_better = None
        if (max_k-min_k)//10 >= 1:
            left_k = [current_k-(2**k*((max_k-min_k)//10)) for k in range(0,resolution) if current_k-(2**k*((max_k-min_k)//10)) >= min_k]
            right_k = [current_k+(2**k*((max_k-min_k)//10)) for k in range(0,resolution) if current_k+(2**k*((max_k-min_k)//10)) <= max_k]
        else:
            left_k = [current_k-k for k in range(1,resolution+1) if current_k-k >= min_k]
            right_k = [current_k+k for k in range(1,resolution+1) if current_k+k <= max_k]
        left_fit = []
        right_fit = []
        for k in left_k:
            if k not in yet_trained:
                t_effective +=1
                t_total +=1
                fit, labels = train_and_fit(data, G, k, vertex_set)
                left_fit.append(fit)
                yet_trained[k] = (fit, labels)
            else:
                t_total +=1
                left_fit.append(yet_trained[k][0])
        for k in right_k:
            if k not in yet_trained:
                t_effective +=1
                t_total +=1
                fit, labels = train_and_fit(data, G, k, vertex_set)
                right_fit.append(fit)
                yet_trained[k] = (fit, labels)
            else:
                t_total +=1
                right_fit.append(yet_trained[k][0])
        if max(left_fit) > max(right_fit):
            where_is_better = 'left'
        elif max(right_fit) > max(left_fit):
            where_is_better = 'right'
        else:
            where_is_better = random.choice(['left','right'])
        if where_is_better == 'left':
            max_k = current_k
            current_k = (min_k + max_k)//2
        else:
            min_k = current_k
            current_k = (min_k + max_k)//2

    for x in range(min_k,max_k+1):
        if x not in yet_trained:
            t_effective +=1
            t_total +=1
            current_fit, current_labels = train_and_fit(data, G, x, vertex_set)
            yet_trained[x] = (current_fit, current_labels)
        else:
            t_total +=1
            current_fit, current_labels = yet_trained[x]
        if current_fit > best_fit:
            best_fit, best_k, best_labels = (current_fit, x, current_labels)
    return (best_k, best_labels, best_fit)

def train_and_fit(data, G, k, vertex_set, **kwargs):
    clustering_labels = agglomerativeClustering(data, n_clusters=k, metric='precomputed', 
                                                linkage='average', memory='aggl-clust-cache')
    clustering_labels_list = clusteringLabelsList(clustering_labels, vertex_set)
    return (nx_comm.modularity(G, clustering_labels_list),clustering_labels)

def agglomerativeClustering(data, threshold=None, metric="euclidean", n_clusters=None, linkage='ward', connectivity=None, memory=None):
    model = AgglomerativeClustering(affinity=metric, linkage=linkage, distance_threshold=threshold, 
                                    n_clusters=n_clusters, connectivity=connectivity, memory=memory)
    model.fit(data)
    labels = model.labels_
    return labels

def clusteringLabelsList(labels, vertex_set):
    label_dict = {}
    for i in range(len(vertex_set)):
        if labels[i] not in label_dict:
            label_dict[labels[i]] = [vertex_set[i]]
        else:
            label_dict[labels[i]].append(vertex_set[i])
    return list(label_dict.values())