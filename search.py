import argparse
import numpy as np
import os
from scipy.spatial.distance import cosine
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt
import re


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


def get_ranked_snapshots(query_id, k, approach, embedding_model, is_human):
    sketch_embedding_path = f"{embedding_model}/sketches-png_embeddings/{query_id}.npy" if not is_human else f"{embedding_model}/sketches-manual-png_embeddings/{query_id.split('_')[0]}_sketch.npy"
    sketch_embedding = load_embedding(sketch_embedding_path)
    
    text_embedding_path = f"{embedding_model}/ImagetoTextOutput_embeddings/{query_id}_GPT4.npy" if not is_human else f"{embedding_model}/camera_queries_embeddings/{query_id.split('_')[0]}.npy"
    text_embedding = load_embedding(text_embedding_path)
    
    snapshot_embeddings_dir = f"{embedding_model}/camera_embeddings/"
    system_text_embeddings_dir = f"{embedding_model}/ImagetoTextOutput_embeddings/"
    sketch_text_embeddings_dir = f"{embedding_model}/{'SketchesImagetoTextOutput_embeddings' if not is_human else 'ManualSketchesImagetoTextOutput_embeddings'}/"
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
                sketch_text_embedding = load_embedding(os.path.join(sketch_text_embeddings_dir, f"{query_id}_GPT4.npy" if not is_human else f"{re.sub("_[0-9]", "_sketch", query_id)}_GPT4.npy"))
                similarity_score = compute_cosine_similarity(sketch_text_embedding, system_text_embedding)
        similarity_scores.append((snapshot_id.split('_')[0], similarity_score))
    
    # Sort based on similarity score in descending order
    ranked_snapshots = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    return ranked_snapshots[:k]


def process_query_id(query_id, k, approach, embedding_model, is_human):
    expected_snapshot_id = query_id.split('_')[0]
    ranked_snapshots = get_ranked_snapshots(query_id=query_id, k=k, approach=approach, embedding_model=embedding_model, is_human=is_human)
    if any(snapshot_id == expected_snapshot_id for snapshot_id, _ in ranked_snapshots):
        return 1
    else:
        return 0


def eval_weighted_sum(query_ids, k, embedding_model, is_human):
    weight_steps = 10

    weighted_sum_top_k_hits = defaultdict(int)

    for step in tqdm(range(0, weight_steps + 1)):
        image_weight = step / weight_steps
        text_weight = 1 - image_weight
        from multiprocessing import Pool
        from functools import partial

        with Pool() as p:
            weighted_sum_top_k_hits[image_weight] = sum(p.map(partial(process_query_id, k=k, approach=WeightedSum(image_weight, text_weight), embedding_model=embedding_model, is_human=is_human), query_ids))
    
    return weighted_sum_top_k_hits


def eval_single_config(query_ids, k, approach, embedding_model, is_human):
    top_k_hits = 0

    from multiprocessing import Pool
    from functools import partial

    with Pool() as p:
        top_k_hits = sum(p.map(partial(process_query_id, k=k, approach=approach, embedding_model=embedding_model, is_human=is_human), query_ids))
    
    return top_k_hits


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--approach', type=str, default='weighted_sum', help='Approach to use for search', choices=['weighted_sum', 'crossmodal', 'image_to_text', 'all'])
    argparser.add_argument('--embedding_model', type=str, default='vertex', help='Embedding model for text and image', choices=['azure', 'vertex'])
    argparser.add_argument('--k', type=int, default=10, help='Top K hits to consider for evaluation')
    argparser.add_argument('--is_human', type=bool, default=False, help='Whether to use human annotations or not')
    args = argparser.parse_args()

    k = args.k
    embedding_model = args.embedding_model
    is_human = args.is_human

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
        top_k_hits = eval_single_config(query_ids, k, approach, embedding_model, is_human)
        print(f"Top k hits for {args.approach} search: {top_k_hits}")
    elif args.approach == 'all':
        blue = '#1D91C0'
        purple = '#8C4F8C'
        orange = '#CC5500'
        title_font_size = 20
        legend_font_size = 14

        human_weighted_sum_top_k_hits = eval_weighted_sum(query_ids, k, embedding_model, is_human=True)
        human_x = list(human_weighted_sum_top_k_hits.keys())
        human_y = [hits / len(query_ids) for hits in human_weighted_sum_top_k_hits.values()]
        human_crossmodal_top_k_hits = eval_single_config(query_ids, k, CrossModal(), embedding_model, is_human=True) / len(query_ids)
        human_image_to_text_top_k_hits = eval_single_config(query_ids, k, ImageToText(), embedding_model, is_human=True) / len(query_ids)
        plt.plot(human_x, human_y, label='Weighted Sum (human)', color=blue, linestyle='-')
        plt.axhline(human_crossmodal_top_k_hits, linestyle='-', color=purple, label='Crossmodal (human)')
        plt.axhline(human_image_to_text_top_k_hits, linestyle='-', color=orange, label='Image to Text (human)')

        machine_weighted_sum_top_k_hits = eval_weighted_sum(query_ids, k, embedding_model, is_human=False)
        machine_x = list(machine_weighted_sum_top_k_hits.keys())
        machine_y = [hits / len(query_ids) for hits in machine_weighted_sum_top_k_hits.values()]
        machine_crossmodal_top_k_hits = eval_single_config(query_ids, k, CrossModal(), embedding_model, is_human=False) / len(query_ids)
        machine_image_to_text_top_k_hits = eval_single_config(query_ids, k, ImageToText(), embedding_model, is_human=False) / len(query_ids)
        plt.plot(machine_x, machine_y, label='Weighted Sum (machine)', color=blue, linestyle='--')
        plt.axhline(machine_crossmodal_top_k_hits, linestyle='--', color=purple, label='Crossmodal (machine)')
        plt.axhline(machine_image_to_text_top_k_hits, linestyle='--', color=orange, label='Image to Text (machine)')
        
        plt.ylim(0, 1)
        plt.xlabel('Image Weight', fontsize=legend_font_size)
        plt.xticks(fontsize=legend_font_size)
        plt.ylabel(f'Percent Top {k} Hits', fontsize=legend_font_size)
        plt.yticks(fontsize=legend_font_size)
        plt.title(f'Percent Top {k} Hits', fontsize=title_font_size)
        plt.legend(loc='upper left' if k < 10 else 'lower left')
        plt.savefig(f'percent_top_{k}_hits_{embedding_model}.png')

if __name__ == "__main__":
    main()
