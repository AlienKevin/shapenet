from typing import List, Optional

import vertexai
from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
    MultiModalEmbeddingResponse,
)

import numpy as np
from numpy.linalg import norm

def cosine_similarity(A, B):
    return np.dot(A,B)/(norm(A)*norm(B))

def get_embedding(
    image_path: Optional[str] = None,
    text: Optional[str] = None,
    project_id: str = 'd-model-search-416919',
    location: str = 'us-central1',
    dimension: int = 1408,
) -> List[float]:
    vertexai.init(project=project_id, location=location)

    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")

    embeddings = model.get_embeddings(
        image=None if image_path is None else Image.load_from_file(image_path),
        contextual_text=text,
        dimension=dimension,
    )
    if image_path is not None:
        return embeddings.image_embedding
    elif text is not None:
        return embeddings.text_embedding

from typing import NamedTuple, Optional

class Entity(NamedTuple):
    name: str
    image_path: Optional[str] = None
    text: Optional[str] = None

from enum import Enum

class Modality(Enum):
    Image = 1
    Text = 2


class Embedding(NamedTuple):
    name: str
    modality: Modality
    embedding: List[float]

    def __str__(self):
        return f"{self.name} ({self.modality.name})"

def compare_cosine_similarity(entities: List[Entity]):
    embeddings = []
    for entity in entities:
        if entity.image_path:
            embedding = get_embedding(image_path=f'samples/{entity.image_path}')
            embeddings.append(Embedding(name=entity.name, modality=Modality.Image, embedding=embedding))
        if entity.text:
            embedding = get_embedding(text=entity.text)
            embeddings.append(Embedding(name=entity.name, modality=Modality.Text, embedding=embedding))

    similarities = []
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            sim = cosine_similarity(embeddings[i].embedding, embeddings[j].embedding)
            similarities.append(((embeddings[i], embeddings[j]), sim))

    # Sort the similarities in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)

    for pair, sim in similarities:
        print(f"Cosine similarity between {pair[0]} and {pair[1]}: {sim:.4f}")

if __name__ == '__main__':

    entities = [
        Entity(name='apple', image_path='apple.png', text='apple'),
        Entity(name='ginkgo1', image_path='ginkgo1.png', text='ginkgo'),
        Entity(name='ginkgo2', image_path='ginkgo2.png', text='maidenhair tree'),
    ]
    compare_cosine_similarity(entities)
