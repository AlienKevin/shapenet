import os
import numpy as np
import requests
import argparse
import hashlib

# Argument parser setup
parser = argparse.ArgumentParser(description='Vectorize text strings from files in a folder and evaluate embeddings.')
parser.add_argument('folder_path', type=str, help='Path to the folder containing text files.')
parser.add_argument('output_folder', type=str, help='Path to the output folder where text files will be saved.')
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
        return np.array(vector)
    except requests.exceptions.RequestException as e:
        print(f"Request failed for text '{text}': {e}")
        return None


def vectorize_texts_in_folder(folder_path, output_folder):
    # Check if the output folder exists, and create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.npy'):  # Ensure we're only processing text files
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            with open(file_path, 'r') as file:
                for line in file:
                    text = line.strip()
                    if text:
                        print(f"Processing text: {text}")
                        text_vector = get_text_embedding(text)
                        if text_vector is not None:
                            # Generate a unique identifier for the text
                            hasher = hashlib.md5()
                            hasher.update(text.encode('utf-8'))
                            hash_id = hasher.hexdigest()
                            # Save the vector to a text file in the output folder
                            vector_filename = os.path.join(output_folder, f"{hash_id}_Azure.npy")
                            np.savetxt(vector_filename, text_vector, fmt='%f')  # Save as text
                            print(f"Vector obtained and saved for text: '{text}'.")
                        else:
                            print(f"Failed to get vector for text: '{text}'.")


if __name__ == "__main__":
    vectorize_texts_in_folder(args.folder_path, args.output_folder)
