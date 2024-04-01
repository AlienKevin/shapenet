import os
import cairosvg

# conda install cairosvg

def convert_svg_to_png():
    sketches_dir = 'sketches/'
    output_dir = 'sketches-png/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(sketches_dir):
        if filename.endswith('.svg'):
            svg_path = os.path.join(sketches_dir, filename)
            png_path = os.path.join(output_dir, filename.replace('.svg', '.png'))
            cairosvg.svg2png(url=svg_path, background_color='white', write_to=png_path)
            print(f"Converted {filename} to PNG in {output_dir}")

if __name__ == "__main__":
    convert_svg_to_png()

