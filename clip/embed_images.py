import subprocess
from pathlib import Path

def calculate_clip_embeddings_for_png_images(image_folder_path, model_path):
    """
    Calculate CLIP embeddings for all png images under the specified folder using the given model.
    
    Parameters:
    - image_folder_path: str, path to the folder containing png images.
    - model_path: str, path to the CLIP model.
    """
    import glob
    png_images = glob.glob(f"{image_folder_path}/*.png")
    for image_path in png_images:
        command = f"./clip.cpp/build/bin/extract -m {model_path} -t 10 --image {image_path}"
        try:
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while calculating CLIP embeddings for {image_path}: {e}")
import os
import glob

def move_img_vec_files_to_embeddings_folder(source_folder_path, destination_folder):
    """
    Move all .npy files starting with 'img_vec' from the source folder to a specified base destination folder.
    
    Parameters:
    - source_folder_path: str, path to the source folder containing .npy files.
    - destination_folder: str, base path for the destination folder where files will be moved.
    """
    destination_folder_path = os.path.join('embeddings', Path(destination_folder).stem)
    os.makedirs(destination_folder_path, exist_ok=True)  # Ensure the destination folder exists
    
    # Find all .npy files starting with 'img_vec' in the source folder
    img_vec_files = glob.glob(os.path.join(source_folder_path, "img_vec_*.npy"))
    
    for file_path in img_vec_files:
        # Move each file to the destination folder
        os.rename(file_path, os.path.join(destination_folder_path, os.path.basename(file_path)))
        print(f"Moved {os.path.basename(file_path)} to {destination_folder_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python embed_images.py <image_folder_path> <destination_folder>")
        sys.exit(1)
    image_folder_path = sys.argv[1]
    destination_folder = sys.argv[2]
    model_path = "models/CLIP-ViT-B-32-laion2B-s34B-b79K_ggml-model-q5_1.gguf"
    calculate_clip_embeddings_for_png_images(image_folder_path, model_path)

    # Call the function after calculating embeddings
    move_img_vec_files_to_embeddings_folder(".", destination_folder)
