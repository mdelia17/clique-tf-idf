# clique-tf-idf

Implementation of clique-tf-idf graph clustering algorithm.
To execute the pipeline, run:

    python pipeline.py -f ifile [OPTIONAL -v -o ofile]
    python pipeline.py -f data/karate.edges -o data/output

the graph in ifile has to be represented by a set of edges (see karate.edges for example) with vertexes ids from 1 to n. 
If ofile is not given, the pipeline will print clustering labels in output.