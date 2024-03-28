import json
import sys
import vertexai
from pathlib import Path

from vertexai.vision_models import Image, MultiModalEmbeddingModel
from vertexai.language_models import TextEmbeddingModel

PROJECT_ID = 'eecs-486-417920'
REGION = "us-central1"

vertexai.init(project=PROJECT_ID, location=REGION)

def text_embeddings(text_json, model='textembedding-gecko@001'):
    model = TextEmbeddingModel.from_pretrained(model) # load model
    embeddings = {}
    with open(text_json, 'r') as file: # load captions
        captions = json.load(file)

    for prefix, text in captions.items(): # get text embeddings
        embedding = model.get_embeddings(
            [text]
        )[0].values
        embeddings[prefix + '_text'] = embedding

    # write to json
    with open(f"{text_json.stem}.text.embeddings.json", 'w', encoding='utf-8') as file:
        json.dump(embeddings, file, indent=4)

def image_embeddings(input_directory, model='multimodalembedding', delimiter='_'):
    model = MultiModalEmbeddingModel.from_pretrained(model) # load model
    embeddings = {}
    for path in input_directory.iterdir(): # get image embeddings
        prefix, viewid = path.stem.rsplit(delimiter, 1)
        embedding = model.get_embeddings(
            image=Image.load_from_file(str(path)),
        ).image_embedding
        embeddings[prefix + '_image_' + viewid] = embedding

    # write to json
    with open(f"{input_directory}.image.embeddings.json", 'w', encoding='utf-8') as file:
        json.dump(embeddings, file, indent=4)

def multimodal_embeddings(text_json, image_directory, model='multimodalembedding', delimiter='_'):
    model = MultiModalEmbeddingModel.from_pretrained(model) # load model
    embeddings = {}
    with open(text_json, 'r') as file: # load captions
        captions = json.load(file)

    for prefix, text in captions.items(): # get text embeddings
        embedding = model.get_embeddings(
            contextual_text=text
        )
        embeddings[prefix + '_text'] = embedding.text_embedding

    for path in image_directory.iterdir(): # get image embeddings
        prefix, viewid = path.stem.rsplit(delimiter, 1)
        embedding = model.get_embeddings(
            image=Image.load_from_file(str(path))
        )
        embeddings[prefix + '_image_' + viewid] = embedding.image_embedding

    # write to json
    with open(f"{image_directory}.{text_json.stem}.multimodal.embeddings.json", 'w', encoding='utf-8') as file:
        json.dump(embeddings, file, indent=4)

def main():
    if PROJECT_ID is None:
        print("Set PROJECT_ID in google_embeddings.py")
        sys.exit(1)

    try:
        embedding_type = sys.argv[1]
    except IndexError:
        print("Usages:")
        print("\tpython3 google_embeddings.py image image_directory")
        print("\tpython3 google_embeddings.py text text_json")
        print("\tpython3 google_embeddings.py multimodal text_json image_directory")
        sys.exit(1)

    if embedding_type not in ('image', 'text', 'multimodal'):
        print(f"Invalid Embedding Type: {embedding_type}")
        sys.exit(1)

    if embedding_type == 'multimodal':
        if len(sys.argv) != 4:
            print("Usage: python3 google_embeddings.py multimodal text_json image_directory")
            sys.exit(1)
        text_directory = Path()/sys.argv[2]
        image_directory = Path()/sys.argv[3]
        if not text_directory.exists():
            print(f"Path does not exist: {text_directory.resolve()}")
            sys.exit(1)
        elif not image_directory.exists():
            print(f"Path does not exist: {image_directory.resolve()}")
            sys.exit(1)

        multimodal_embeddings(text_directory, image_directory) # generate multimodal embeddings
    else:
        if len(sys.argv) != 3:
            print("Usages:")
            print("\tpython3 google_embeddings.py image image_directory")
            print("\tpython3 google_embeddings.py text text_json")
            sys.exit(1)
        input_path = Path()/sys.argv[2]
        if not input_path.exists():
            print(f"Path does not exist: {input_path.resolve()}")
            sys.exit(1)

        if embedding_type == 'image':
            image_embeddings(input_path) # generate image embeddings
        else:
            text_embeddings(input_path) # generate text embeddings

if __name__ == '__main__':
    main()
