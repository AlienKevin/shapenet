import os
import numpy as np
import requests
import argparse
import hashlib

# Argument parser setup
parser = argparse.ArgumentParser(description='Vectorize local images and evaluate embeddings.')
parser.add_argument('folder_path', type=str, help='Path to the folder containing local image files.')
args = parser.parse_args()

# Azure Cognitive Services credentials and endpoint
endpoint = os.getenv("VISION_ENDPOINT", "https://image-recog.cognitiveservices.azure.com/")
key = os.getenv("VISION_KEY", "fb717a91a8d6419482be08619d1a4b48")

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

def vectorize_images_in_folder(folder_path, embeddings_folder="embeddings"):
    os.makedirs(embeddings_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            image_vector = get_image_embedding(img_path)
            if image_vector:
                # Generate a hash of the filename for a unique but consistent identifier
                filename_hash = hashlib.md5(filename.encode()).hexdigest()
                # Save each embedding in a separate .txt file
                embedding_file_path = os.path.join(embeddings_folder, f"{filename_hash}_Azure_camera.npy")
                with open(embedding_file_path, "w") as file:
                    for value in image_vector:
                        file.write(f"{value}\n")
                print(f"Vector saved for {filename} as {embedding_file_path}.")
            else:
                print(f"Failed to get vector for {filename}.")

if __name__ == "__main__":
    vectorize_images_in_folder(args.folder_path)
