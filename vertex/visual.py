import json
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Load the embeddings from the JSON file
with open("embeddings.json", "r") as f:
    embeddings_dict = json.load(f)

# Convert the embeddings to a NumPy array
embeddings = np.array(list(embeddings_dict.values()))

# Apply t-SNE for dimensionality reduction
tsne = TSNE(n_components=2, random_state=42)
reduced_embeddings = embeddings

# Create a scatter plot of the reduced embeddings
plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])

# Add labels to the points with file names
for filename, embedding in embeddings_dict.items():
    plt.annotate(filename, xy=(embedding[0], embedding[1]), xytext=(5, 5),
                 textcoords='offset points', ha='left', va='bottom')

plt.title("t-SNE Visualization of Embeddings")
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.tight_layout()
plt.show()
