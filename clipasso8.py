import replicate
from urllib.request import urlretrieve

import asyncio

image_names = [
    "ball-shaped camera 1",
    "ball-shaped camera 2",
    "ball-shaped camera 5",
    "CCTV camera 1",
    "CCTV camera 2",
    "CCTV camera 5",
    "classic film camera 1",
    "classic film camera 2",
    "classic film camera 5",
    "DSLR camera 1",
    "DSLR camera 2",
    "DSLR camera 5",
]

async def run_clipasso_concurrently():
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(replicate.async_run(
                "yael-vinker/clipasso:9890b0260cd82faa230db114406dc5a3b26fc0f940fb6057158b4747e22bf320",
                input={
                    "target_image": open(f"images/{name}.png", 'rb'),
                    "trials": 1,
                    "fix_scale": 0,
                    "mask_object": 0,
                    "num_strokes": 8
                }))
            for name in image_names
        ]

    results = await asyncio.gather(*tasks)

    for image_name, output in zip(image_names, results):
        print(image_name)
        print(output)
        urlretrieve(output, f"sketches8/{image_name}.svg")

asyncio.run(run_clipasso_concurrently())
