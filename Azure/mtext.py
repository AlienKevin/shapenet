import os
import numpy as np
import requests
import argparse
import json

# Argument parser setup
parser = argparse.ArgumentParser(description='Vectorize text strings from files in a folder and evaluate embeddings.')
parser.add_argument('folder_path', type=str, help='Path to the folder containing text files.')
args = parser.parse_args()

# Azure Cognitive Services credentials and endpoint
endpoint = os.getenv("VISION_ENDPOINT", "https://image-recog.cognitiveservices.azure.com/")
key = os.getenv("VISION_KEY", "fb717a91a8d6419482be08619d1a4b48")

def get_text_embedding(text):
    vectorize_text_url = f"{endpoint}/computervision/retrieval:vectorizeText?api-version=2023-02-01-preview&model-version=2023-04-15"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }

    try:
        response = requests.post(vectorize_text_url, headers=headers, json=payload)
        response.raise_for_status()
        vector = response.json().get('vector', None)
        return vector
    except requests.exceptions.RequestException as e:
        print(f"Request failed for text '{text}': {e}")
        return None

def vectorize_texts_in_folder(folder_path):
    embeddings = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            with open(file_path, 'r') as file:
                for line in file:
                    text = line.strip()
                    if text:
                        print(f"Processing text: {text}")
                        text_vector = get_text_embedding(text)
                        if text_vector:
                            embeddings[text] = text_vector
                            print(f"Vector obtained for text: '{text}'.")
                        else:
                            print(f"Failed to get vector for text: '{text}'.")
    return embeddings

if __name__ == "__main__":
    embeddings = vectorize_texts_in_folder(args.folder_path)
    output_file = "text_embeddings.json"
    with open(output_file, "w") as file:
        json.dump(embeddings, file, indent=4)
    print(f"Embeddings saved to {output_file}")