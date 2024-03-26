import argparse
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

def generate_image_caption(image_path):
    # Load the BLIP model and processor
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

    # Open the image file
    image = Image.open(image_path)

    # Preprocess the image and generate captions
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs)

    # Decode the generated captions
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

def write_output(output_path, caption):
    """Writes the caption to an output file."""
    with open(output_path, 'w') as file:
        file.write(f"Caption: {caption}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a caption for an image.")
    parser.add_argument("image_path", type=str, help="Path to the image file")

    args = parser.parse_args()

    caption = generate_image_caption(args.image_path)
    
    # Construct the output file name
    base_name = os.path.splitext(args.image_path)[0]
    output_file_path = f"{base_name}.huggingface.output"
    
    # Write the caption to the output file
    write_output(output_file_path, caption)

    print(f"Caption written to {output_file_path}")
