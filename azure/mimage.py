import os
import numpy as np
import requests
import argparse
import json

# Argument parser setup
parser = argparse.ArgumentParser(description='Vectorize local images and evaluate embeddings.')
parser.add_argument('folder_path', type=str, help='Path to the folder containing local image files.')
args = parser.parse_args()

# Azure Cognitive Services credentials and endpoint
endpoint = os.getenv("VISION_ENDPOINT", xxx")
key = os.getenv("VISION_KEY", "xxx")

def get_image_embedding(image_path):
    vectorize_img_url = f"{endpoint}/computervision/retrieval:vectorizeImage?api-version=2023-02-01-preview&model-version=2023-04-15"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"
    }

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            response = requests.post(vectorize_img_url, headers=headers, data=image_data)
            response.raise_for_status()
            vector = response.json().get('vector', None)
            return vector
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {image_path}: {e}")
        return None

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def vectorize_images_in_folder(folder_path):
    embeddings = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            image_vector = get_image_embedding(img_path)
            if image_vector:
                embeddings[filename] = image_vector
                print(f"Vector obtained for {filename}.")
            else:
                print(f"Failed to get vector for {filename}.")
    return embeddings

def save_embeddings_to_json(embeddings, output_file="embeddings.json"):
    with open(output_file, "w") as file:
        json.dump(embeddings, file)

def load_embeddings_from_json(input_file="embeddings.json"):
    with open(input_file, "r") as file:
        return json.load(file)


def calculate_similarities(embeddings):
    filenames = list(embeddings.keys())
    with open("similarities.txt", 'w') as f:
        for i in range(len(filenames)):
            for j in range(i+1, len(filenames)):
                sim = cosine_similarity(embeddings[filenames[i]], embeddings[filenames[j]])
                f.write(f"Cosine similarity between {filenames[i]} and {filenames[j]}: {sim}\n")

if __name__ == "__main__":
    embeddings = vectorize_images_in_folder(args.folder_path)
    save_embeddings_to_json(embeddings)
    embeddings_loaded = load_embeddings_from_json()
    calculate_similarities(embeddings_loaded)
