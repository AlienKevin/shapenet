import argparse
import numpy as np
import os
from scipy.spatial.distance import cosine
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt


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


def get_ranked_snapshots(query_id, k, approach, embedding_model):
    sketch_embedding_path = f"{embedding_model}/sketches-png_embeddings/{query_id}.npy"
    sketch_embedding = load_embedding(sketch_embedding_path)
    
    text_embedding_path = f"{embedding_model}/ImagetoTextOutput_embeddings/{query_id}_GPT4.npy"
    text_embedding = load_embedding(text_embedding_path)
    
    snapshot_embeddings_dir = f"{embedding_model}/camera_embeddings/"
    system_text_embeddings_dir = f"{embedding_model}/ImagetoTextOutput_embeddings/"
    sketch_text_embeddings_dir = f"{embedding_model}/SketchesImagetoTextOutput_embeddings/"
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


def process_query_id(query_id, k, approach, embedding_model):
    expected_snapshot_id = query_id.split('_')[0]
    ranked_snapshots = get_ranked_snapshots(query_id=query_id, k=k, approach=approach, embedding_model=embedding_model)
    if any(snapshot_id == expected_snapshot_id for snapshot_id, _ in ranked_snapshots):
        return 1
    else:
        return 0


def eval_weighted_sum(query_ids, k, embedding_model):
    weight_steps = 10

    weighted_sum_top_k_hits = defaultdict(int)

    for step in tqdm(range(0, weight_steps + 1)):
        image_weight = step / weight_steps
        text_weight = 1 - image_weight
        from multiprocessing import Pool
        from functools import partial

        with Pool() as p:
            weighted_sum_top_k_hits[image_weight] = sum(p.map(partial(process_query_id, k=k, approach=WeightedSum(image_weight, text_weight), embedding_model=embedding_model), query_ids))
    
    return weighted_sum_top_k_hits


def eval_single_config(query_ids, k, approach, embedding_model):
    top_k_hits = 0

    from multiprocessing import Pool
    from functools import partial

    with Pool() as p:
        top_k_hits = sum(p.map(partial(process_query_id, k=k, approach=approach, embedding_model=embedding_model), query_ids))
    
    return top_k_hits


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--approach', type=str, default='weighted_sum', help='Approach to use for search', choices=['weighted_sum', 'crossmodal', 'image_to_text', 'all'])
    argparser.add_argument('--embedding_model', type=str, default='vertex', help='Embedding model for text and image', choices=['azure', 'vertex'])
    argparser.add_argument('--k', type=int, default=10, help='Top K hits to consider for evaluation')
    args = argparser.parse_args()

    k = args.k
    embedding_model = args.embedding_model

    query_ids = []
    for root, dirs, files in os.walk(f'{embedding_model}/sketches-png_embeddings'):
        for file in files:
            query_ids.append(Path(file).stem)

    if args.approach == 'weighted_sum':
        weighted_sum_top_k_hits = eval_weighted_sum(query_ids, k, embedding_model)

        print(weighted_sum_top_k_hits)

        x = list(weighted_sum_top_k_hits.keys())
        y = list(weighted_sum_top_k_hits.values())

        plt.plot(x, y)
        plt.xlabel('Weight')
        plt.ylabel('Top k Hits')
        plt.title('Top k Hits vs Image Weight')
        plt.savefig('weighted_sum_top_k_hits.png')
    elif args.approach == 'crossmodal' or args.approach == 'image_to_text':
        approach = CrossModal() if args.approach == 'crossmodal' else ImageToText()
        top_k_hits = eval_single_config(query_ids, k, approach, embedding_model)
        print(f"Top k hits for {args.approach} search: {top_k_hits}")
    elif args.approach == 'all':
        weighted_sum_top_k_hits = eval_weighted_sum(query_ids, k, embedding_model)

        x = list(weighted_sum_top_k_hits.keys())
        y = [hits / len(query_ids) for hits in weighted_sum_top_k_hits.values()]

        crossmodal_top_k_hits = eval_single_config(query_ids, k, CrossModal(), embedding_model) / len(query_ids)
        image_to_text_top_k_hits = eval_single_config(query_ids, k, ImageToText(), embedding_model) / len(query_ids)

        plt.plot(x, y, label='Weighted Sum')
        plt.axhline(crossmodal_top_k_hits, linestyle='-', color='green', label='Crossmodal')
        plt.axhline(image_to_text_top_k_hits, linestyle='-', color='red', label='Image to Text')
        plt.xlabel('Image Weight')
        plt.ylabel(f'Percent Top {k} Hits')
        plt.title(f'Percent Top {k} Hits')
        plt.legend(loc='center left')
        plt.savefig(f'percent_top_{k}_hits_{embedding_model}.png')

if __name__ == "__main__":
    main()
