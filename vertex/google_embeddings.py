import click
import sys
import vertexai
from pathlib import Path
import numpy as np
import shutil

from vertexai.vision_models import Image, MultiModalEmbeddingModel

PROJECT_ID = ''
REGION = ""

vertexai.init(project=PROJECT_ID, location=REGION)

VERTEX_ROOT = Path(__file__).resolve().parent

def generate_text_embeddings(txt_dir, model):
    model = MultiModalEmbeddingModel.from_pretrained(model)
    text_output_directory = VERTEX_ROOT/f"{txt_dir.stem}_embeddings"
    if text_output_directory.exists():
        shutil.rmtree(text_output_directory)
    text_output_directory.mkdir()
    for file in txt_dir.iterdir():
        embedding = model.get_embeddings(
            contextual_text=file.read_text()
        )

        output_file = text_output_directory/f"{file.stem}.npy"
        with output_file.open(mode='w') as file:
            np.savetxt(file, embedding.text_embedding)

def generate_image_embeddings(img_dir, model):
    model = MultiModalEmbeddingModel.from_pretrained(model)
    image_output_directory = VERTEX_ROOT/f"{img_dir.stem}_embeddings"
    if image_output_directory.exists():
        shutil.rmtree(image_output_directory)
    image_output_directory.mkdir()
    for file in img_dir.iterdir():
        embedding = model.get_embeddings(
            image=Image.load_from_file(str(file))
        )

        output_file = image_output_directory/f"{file.stem}.npy"
        with output_file.open(mode='w') as file:
            np.savetxt(file, embedding.image_embedding)

def multimodal_embeddings(txt_dirs, img_dirs, model='multimodalembedding'):
    for txt_dir in txt_dirs:
        generate_text_embeddings(txt_dir, model)

    for img_dir in img_dirs:
        generate_image_embeddings(img_dir, model)
    sys.exit(1)

@click.command()
@click.option('--img_dir', '-i', "img_dirs", default=None, multiple=True, help='Image Directory Path')
@click.option('--txt_dir', '-t', "txt_dirs", default=None, multiple=True, help='Text Directory Path')
def main(img_dirs, txt_dirs):
    if img_dirs is None and txt_dirs is None:
        print("No directory paths provided")
        sys.exit(1)

    if PROJECT_ID is None:
        print("Set PROJECT_ID in google_embeddings.py")
        sys.exit(1)

    img_dirs = [Path()/img_dir for img_dir in img_dirs]
    txt_dirs = [Path()/txt_dir for txt_dir in txt_dirs]

    dne = []
    for img_dir in img_dirs:
        if not img_dir.exists():
            dne.append(str(img_dir.resolve()))
    for txt_dir in txt_dirs:
        if not txt_dir.exists():
            dne.append(str(txt_dir.resolve()))

    if len(dne) > 0:
        print("The following directories do not exist:")
        print(('\n').join(dne))
        sys.exit(1)

    multimodal_embeddings(txt_dirs, img_dirs)

if __name__ == '__main__':
    main()
