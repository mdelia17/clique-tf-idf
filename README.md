# Clique-TF-IDF

Implementation of Clique-TF-IDF graph clustering algorithm, as discussed in [D’Elia, M., Finocchi, I., Patrignani, M. (2023). Clique-TF-IDF: A New Partitioning Framework Based on Dense Substructures. AIxIA 2023 – Advances in Artificial Intelligence. AIxIA 2023. Lecture Notes in Computer Science(), vol 14318. Springer](https://link.springer.com/chapter/10.1007/978-3-031-47546-7_27)

## Usage

To run the pipeline, run:

    python pipeline.py -f ifile [OPTIONAL -v -o ofile -k blocks]
    python pipeline.py -f data/karate.edges -o data/output

The graph in ifile has to be represented by a set of edges (see karate.edges for example) with vertexes ids from 1 to n. 
If ofile is not given, the pipeline will print clustering labels in output. If k is invalid or not specified, the pipeline will find its best value.

## Citing

If you find Clique-TF-IDF useful in your research, please cite the following paper:

    @inproceedings{d2023clique,
    title={Clique-TF-IDF: A New Partitioning Framework Based on Dense Substructures},
    author={D’Elia, Marco and Finocchi, Irene and Patrignani, Maurizio},
    booktitle={International Conference of the Italian Association for Artificial Intelligence},
    pages={396--410},
    year={2023},
    organization={Springer}
    }


