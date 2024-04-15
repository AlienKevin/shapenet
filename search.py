import argparse
import numpy as np
import os
from scipy.spatial.distance import cosine
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

def load_embedding(file_path):
    return np.loadtxt(file_path)

def compute_cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

from dataclasses import dataclass

class Approach:
    pass

@dataclass
class WeightedSum(Approach):
    image_weight: float
    text_weight: float

class CrossModal(Approach):
    pass

class ImageToText(Approach):
    pass

def get_ranked_snapshots(query_id, k, approach):
    sketch_embedding_path = f"vertex/sketches-png_embeddings/{query_id}.npy"
    sketch_embedding = load_embedding(sketch_embedding_path)
    
    text_embedding_path = f"vertex/ImagetoTextOutput_embeddings/{query_id}_GPT4.npy"
    text_embedding = load_embedding(text_embedding_path)
    
    snapshot_embeddings_dir = "vertex/camera_embeddings/"
    system_text_embeddings_dir = "vertex/ImagetoTextOutput_embeddings/"
    sketch_text_embeddings_dir = "vertex/SketchesImagetoTextOutput_embeddings/"
    similarity_scores = []
    
    for snapshot_file in os.listdir(snapshot_embeddings_dir):
        snapshot_id = snapshot_file.split('.')[0]
        snapshot_embedding_path = os.path.join(snapshot_embeddings_dir, snapshot_file)
        snapshot_embedding = load_embedding(snapshot_embedding_path)
        
        system_text_embedding_path = os.path.join(system_text_embeddings_dir, f"{snapshot_id}_Gemmini.npy")
        if os.path.exists(system_text_embedding_path):
            system_text_embedding = load_embedding(system_text_embedding_path)
        else:
            # print(f"Gemini embedding not found for snapshot {snapshot_id}")
            system_text_embedding = np.ones_like(text_embedding)

        match approach:
            case WeightedSum(image_weight=image_weight, text_weight=text_weight):
                image_similarity_score = compute_cosine_similarity(sketch_embedding, snapshot_embedding)
                text_similarity_score = compute_cosine_similarity(text_embedding, system_text_embedding)
                similarity_score = image_weight * image_similarity_score + text_weight * text_similarity_score
            case CrossModal():
                sketch_system_text_similarity_score = compute_cosine_similarity(sketch_embedding, system_text_embedding)
                similarity_score = max(sketch_system_text_similarity_score, compute_cosine_similarity(text_embedding, snapshot_embedding))
            case ImageToText():
                sketch_text_embedding = load_embedding(os.path.join(sketch_text_embeddings_dir, f"{query_id}_GPT4.npy"))
                similarity_score = compute_cosine_similarity(sketch_text_embedding, system_text_embedding)
        similarity_scores.append((snapshot_id.split('_')[0], similarity_score))
    
    # Sort based on similarity score in descending order
    ranked_snapshots = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    return ranked_snapshots[:k]

def process_query_id(query_id, k, approach):
    expected_snapshot_id = query_id.split('_')[0]
    ranked_snapshots = get_ranked_snapshots(query_id=query_id, k=k, approach=approach)
    if any(snapshot_id == expected_snapshot_id for snapshot_id, _ in ranked_snapshots):
        return 1
    else:
        return 0

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--approach', type=str, default='weighted_sum', help='Approach to use for search', choices=['weighted_sum', 'crossmodal', 'image_to_text'])

    args = argparser.parse_args()

    k = 10

    query_ids = []

    for root, dirs, files in os.walk('vertex/sketches-png_embeddings'):
        for file in files:
            query_ids.append(Path(file).stem)

    if args.approach == 'weighted_sum':
        weight_steps = 10

        weighted_sum_top_k_hits = defaultdict(int)

        for step in tqdm(range(0, weight_steps + 1)):
            image_weight = step / weight_steps
            text_weight = 1 - image_weight
            from multiprocessing import Pool
            from functools import partial

            with Pool() as p:
                weighted_sum_top_k_hits[image_weight] = sum(p.map(partial(process_query_id, k=k, approach=WeightedSum(image_weight, text_weight)), query_ids))

        print(weighted_sum_top_k_hits)

        import matplotlib.pyplot as plt

        x = list(weighted_sum_top_k_hits.keys())
        y = list(weighted_sum_top_k_hits.values())

        plt.plot(x, y)
        plt.xlabel('Weight')
        plt.ylabel('Top k Hits')
        plt.title('Top k Hits vs Image Weight')
        plt.savefig('weighted_sum_top_k_hits.png')
    elif args.approach == 'crossmodal' or args.approach == 'image_to_text':
        top_k_hits = 0

        approach = CrossModal() if args.approach == 'crossmodal' else ImageToText()

        from multiprocessing import Pool
        from functools import partial

        with Pool() as p:
            top_k_hits = sum(p.map(partial(process_query_id, k=k, approach=approach), query_ids))

        print(f"Top k hits for {args.approach} search: {top_k_hits}")

if __name__ == "__main__":
    main()
