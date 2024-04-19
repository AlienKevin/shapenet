import os
import sys
import subprocess

def run_scripts(image_path):
    # Run the first script
    subprocess.run(["python", "GPTimagetotext.py", image_path])

    # Run the second script
    subprocess.run(["python", "Geminiimagetotext.py", image_path])

def main():
    if len(sys.argv) != 2:
        print("Usage: python driver.py <path_to_input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, filename)
            run_scripts(image_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    main()
