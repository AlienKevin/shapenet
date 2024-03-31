import replicate
from urllib.request import urlretrieve
import asyncio
import random
import os
import re

random.seed(0)

# List all files in the snapshots/camera directory
all_images = sorted(os.listdir("snapshots/camera"))

# Filter out files that don't match the expected pattern (name_number.png)
pattern = re.compile(r"(.+)_(\d+)\.png")
filtered_images = [img for img in all_images if pattern.match(img)]

# Group images by their base name (before the underscore) and select images based on thirds
image_groups = {}
for image in filtered_images:
    match = pattern.match(image)
    base_name, number = match.groups()
    image_name = base_name + "_" + number
    if base_name in image_groups:
        image_groups[base_name].append(image_name)
    else:
        image_groups[base_name] = [image_name]

# Sort each group and select images based on thirds
image_names = []
groups = list(image_groups.values())
random.shuffle(groups)
for i, images in enumerate(groups):
    if i < len(groups) / 3:
        image_names.append(images[0])
    elif i < len(groups) * 2 / 3:
        image_names.append(images[1])
    else:
        image_names.append(images[2])


assert(len(image_names) == len(filtered_images) / 3)

async def run_clipasso_concurrently():
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(replicate.async_run(
                "yael-vinker/clipasso:9890b0260cd82faa230db114406dc5a3b26fc0f940fb6057158b4747e22bf320",
                input={
                    "target_image": open(f"snapshots/camera/{name}.png", 'rb'),
                    "trials": 1,
                    "fix_scale": 0,
                    "mask_object": 0,
                    "num_strokes": 16
                }))
            for name in image_names
        ]

    results = await asyncio.gather(*tasks)

    for image_name, output in zip(image_names, results):
        print(image_name)
        print(output)
        urlretrieve(output, f"sketches/{image_name}.svg")

asyncio.run(run_clipasso_concurrently())
