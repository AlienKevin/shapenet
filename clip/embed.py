import numpy as np
from scipy.spatial.distance import cosine
import os
import matplotlib.pyplot as plt
import seaborn as sns

def load_clip_embeddings_from_folder(folder_path):
    """
    Load all CLIP embeddings from .npy files in a given folder, along with their names.
    
    Parameters:
    - folder_path: str, path to the folder containing .npy files with CLIP embeddings.
    
    Returns:
    - embeddings_list: list of numpy.ndarray, list containing loaded CLIP embeddings from all files.
    - names: list of str, list containing the names extracted from .npy file names.
    """
    embeddings_list = []
    names = []
    for file in sorted(os.listdir(folder_path)):
        if file.endswith(".npy"):
            file_path = os.path.join(folder_path, file)
            embeddings = np.load(file_path)
            embeddings_list.append(embeddings)
            names.append(file.replace('.npy', ''))
    return embeddings_list, names

def calculate_cosine_similarity_between_all(embeddings_list):
    """
    Calculate cosine similarity between each pair of embeddings across all provided embeddings.
    
    Parameters:
    - embeddings_list: list of numpy.ndarray, list containing CLIP embeddings from all files.
    
    Returns:
    - similarity_matrix: numpy.ndarray, matrix of cosine similarity scores for each embeddings pair.
    """
    num_embeddings = len(embeddings_list)
    similarity_matrix = np.zeros((num_embeddings, num_embeddings))
    
    for i in range(num_embeddings):
        for j in range(i, num_embeddings):
            embeddings_i = embeddings_list[i]
            embeddings_j = embeddings_list[j]
            similarity = 1 - cosine(embeddings_i.mean(axis=0), embeddings_j.mean(axis=0))
            similarity_matrix[i, j] = similarity
            similarity_matrix[j, i] = similarity  # Symmetric matrix
    
    return similarity_matrix

def plot_similarity_matrix(similarity_matrix, names):
    """
    Plot a colored similarity matrix.
    
    Parameters:
    - similarity_matrix: numpy.ndarray, matrix of cosine similarity scores.
    - names: list of str, list containing the names for the matrix axes.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(similarity_matrix, annot=True, fmt=".2f", cmap='coolwarm', xticklabels=names, yticklabels=names)
    plt.title("Cosine Similarity Between Embeddings")
    plt.show()

import sys

if __name__ == "__main__":
    embeddings_folder_path = sys.argv[1]
    embeddings_list, names = load_clip_embeddings_from_folder(embeddings_folder_path)
    similarity_matrix = calculate_cosine_similarity_between_all(embeddings_list)
    plot_similarity_matrix(similarity_matrix, names)
