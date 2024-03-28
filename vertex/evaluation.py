import sys
import json
from collections import defaultdict

import numpy
from numpy.linalg import norm

def cos_sim(x, y):
    return numpy.dot(x, y) / (norm(x) * norm(y))

def evaluate_cluster(cluster):
    if len(cluster) > 1: # cluster statistics
        cos_sim_list = []
        for i in range(0, len(cluster), 1):
            for j in range(i+1, len(cluster), 1):
                cos_sim_list.append(cos_sim(cluster[i], cluster[j]))
        return (max(cos_sim_list), min(cos_sim_list))
    return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 evaluation.py json_file")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        embeddings = json.load(file)

    clusters = defaultdict(list)
    # group embeddings by prefix
    for name, embedding in embeddings.items():
        prefix, _, _ = name.partition('_')
        clusters[prefix].append(embedding)

    spreads = []
    for prefix, cluster in clusters.items():
        evaluation = evaluate_cluster(cluster)
        if evaluation is not None:
            _max, _min = evaluation
            spread = _max - _min
            spreads.append(spread)
            print(prefix)
            print(f"\tMax Cosine Similarity: {_max}")
            print(f"\tMin Cosine Similarity: {_min}")
            print(f"\tSpread               : {spread}")
            print()

    print("Summeray")
    print(f"Average Spread: {numpy.mean(spreads)}")



if __name__ == '__main__':
    main()
