import replicate
from urllib.request import urlretrieve

for prediction in sorted(replicate.predictions.list(), key=lambda x: x.created_at):
    svg_url = prediction.output
    if prediction.output is not None:
        print("prediction.created_at: ", prediction.created_at, "prediction.id: ", prediction.id)
        # image_name = prediction.id + ".svg"
        # urlretrieve(svg_url, f"downloads/{image_name}")
        # print(f"Downloaded {image_name}")
