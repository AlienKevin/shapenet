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
reduced_embeddings = tsne.fit_transform(embeddings)

# Create a scatter plot of the reduced embeddings
plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])

with open("captions.json", "r") as f:
    captions = json.load(f)

def to_readable_name(name):
    id, next = name.split("_", 1)
    return captions[id] + "_" + next

# Add labels to the points
for i, name in enumerate(embeddings_dict.keys()):
    plt.annotate(to_readable_name(name), xy=(reduced_embeddings[i, 0], reduced_embeddings[i, 1]), xytext=(5, 5),
                 textcoords='offset points', ha='left', va='bottom')

plt.title("t-SNE Visualization of Embeddings")
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.tight_layout()
plt.show()
