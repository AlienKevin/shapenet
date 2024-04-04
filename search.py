import numpy as np
import os
import argparse
from scipy.spatial.distance import cosine

def load_embedding(file_path):
    return np.loadtxt(file_path)

def compute_cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

def get_ranked_snapshots(query_id, k=10):
    print(query_id)
    sketch_embedding_path = f"vertex/sketches-png_embeddings/{query_id}.npy"
    sketch_embedding = load_embedding(sketch_embedding_path)
    
    text_embedding_path = f"vertex/ImagetoTextOutput_embeddings/{query_id}_GPT4.npy"
    text_embedding = load_embedding(text_embedding_path)
    
    snapshot_embeddings_dir = "vertex/camera_embeddings/"
    system_text_embeddings_dir = "vertex/ImagetoTextOutput_embeddings/"
    similarity_scores = []
    
    for snapshot_file in os.listdir(snapshot_embeddings_dir):
        snapshot_id = snapshot_file.split('.')[0]
        snapshot_embedding_path = os.path.join(snapshot_embeddings_dir, snapshot_file)
        snapshot_embedding = load_embedding(snapshot_embedding_path)
        
        system_text_embedding_path = os.path.join(system_text_embeddings_dir, f"{snapshot_id}_Gemmini.npy")

        image_similarity_score = compute_cosine_similarity(sketch_embedding, snapshot_embedding)
        
        if os.path.exists(system_text_embedding_path):
            system_text_embedding = load_embedding(system_text_embedding_path)
            text_similarity_score = compute_cosine_similarity(text_embedding, system_text_embedding)
        else:
            print(f"Gemini embedding not found for snapshot {snapshot_id}")
            text_similarity_score = 0
        
        weighted_similarity_score = 0.5 * image_similarity_score + 0.5 * text_similarity_score
        similarity_scores.append((snapshot_id, weighted_similarity_score))
    
    # Sort based on similarity score in descending order
    ranked_snapshots = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    return ranked_snapshots[:k]

def main():
    parser = argparse.ArgumentParser(description='Find closest snapshots to a given sketch.')
    parser.add_argument('query_id', type=str, help='ID of the sketch and text')
    parser.add_argument('--k', type=int, default=10, help='Number of top results to return')
    
    args = parser.parse_args()
    
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider
    
    ranked_snapshots = get_ranked_snapshots(args.query_id, args.k)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(left=0.25, bottom=0.25)
    
    # Initially display the first image
    snapshot_id, score = ranked_snapshots[0]
    img = plt.imread(f'snapshots/camera/{snapshot_id}.png')
    im_display = ax.imshow(img)
    ax.set_title(f"Snapshot ID: {snapshot_id}, Similarity Score: {score}")
    ax.axis('off')  # Hide axes
    
    # Slider
    axcolor = 'lightgoldenrodyellow'
    ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Snapshot', 0, len(ranked_snapshots)-1, valinit=0, valfmt='%0.0f')
    
    def update(val):
        index = int(slider.val)
        snapshot_id, score = ranked_snapshots[index]
        img = plt.imread(f'snapshots/camera/{snapshot_id}.png')
        im_display.set_data(img)
        ax.set_title(f"Snapshot ID: {snapshot_id}, Similarity Score: {score}")
        fig.canvas.draw_idle()
    
    slider.on_changed(update)
    
    plt.show()

if __name__ == "__main__":
    main()
