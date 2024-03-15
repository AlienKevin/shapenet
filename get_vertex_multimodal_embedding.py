from typing import List, Optional
import json

import vertexai
from vertexai.vision_models import (
    Image,
    MultiModalEmbeddingModel,
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

def get_embeddings(entities: List[Entity]):
    embeddings = []
    for entity in entities:
        if entity.image_path:
            embedding = get_embedding(image_path=entity.image_path)
            embeddings.append(Embedding(name=entity.name, modality=Modality.Image, embedding=embedding))
        if entity.text:
            embedding = get_embedding(text=entity.text)
            embeddings.append(Embedding(name=entity.name, modality=Modality.Text, embedding=embedding))
    return embeddings

if __name__ == '__main__':
    entities = []

    with open("captions.json", "r") as f:
        captions = json.load(f)
        for id, caption in captions.items():
            for i in range(1, 7):
                entities.append(Entity(name=f'{id}_image_{i}', image_path=f'snapshots/{id}_{i}.png'))
            entities.append(Entity(name=f'{id}_text', text=caption))

    embeddings = get_embeddings(entities)

    embs = {}
    for embedding in embeddings:
        embs[embedding.name] = embedding.embedding

    with open("embeddings.json", "w") as f:
        json.dump(embs, f, indent=4)
