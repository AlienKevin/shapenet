import json
import shutil
import os

with open('captions.json', 'r') as f:
    captions = json.load(f)

if os.path.exists('images'):
    shutil.rmtree('images')

# Create the images directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Loop through each caption and its corresponding images
for id, caption in captions.items():
    for i in range(1, 7):  # Assuming there are 6 images per caption
        src_path = f'snapshots/{id}_{i}.png'
        dst_path = f'images/{caption} {i}.png'
        # Copy the image from snapshots to images folder
        shutil.copy(src_path, dst_path)
