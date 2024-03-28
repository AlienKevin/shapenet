import sys
import numpy as np
import json


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    similarity = dot_product / norm_product if norm_product else 0
    return similarity


def calculate_max_cosine_difference_score(embeddings_by_model):
    max_cosine_diff = 0
    total_comparisons = 0
    total_pairs = 0

    # Calculate the total number of pairs
    models = list(embeddings_by_model.keys())
    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            total_pairs += len(embeddings_by_model[models[i]]) * len(embeddings_by_model[models[j]])

    # Iterate over each unique pair of models to compare their embeddings
    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            model_i_embeddings = embeddings_by_model[models[i]]
            model_j_embeddings = embeddings_by_model[models[j]]
            # Calculate pairwise cosine similarities and find the minimum (maximum difference)
            for vec_i in model_i_embeddings:
                for vec_j in model_j_embeddings:
                    cosine_sim = cosine_similarity(vec_i, vec_j)
                    cosine_diff = 1 - cosine_sim  # Since cosine similarity ranges from -1 to 1
                    max_cosine_diff = max(max_cosine_diff, cosine_diff)
                    total_comparisons += 1
                    percentage = (total_comparisons / total_pairs) * 100
                    print(f"Comparing embeddings: {total_comparisons}/{total_pairs} ({percentage:.2f}%)", end='\r')

    # Scale the maximum cosine difference to a score between 1 and 100
    score = max_cosine_diff * 100
    print("\nDone!")
    print("Maximum cosine difference score:", score)
    return score


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <embedding_file>")
        sys.exit(1)

    embedding_file = sys.argv[1]

    # Load embeddings from the JSON file
    with open(embedding_file, 'r') as f:
        embeddings_by_model = json.load(f)

    calculate_max_cosine_difference_score(embeddings_by_model)
