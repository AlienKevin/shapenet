from PIL import Image  # For image handling
import google.generativeai as genai
import sys  # For command-line arguments

# Replace with your actual API key
API_KEY = "AIzaSyD0aJ2ju1Tgi6tb6_KL28gh65eNQdHbWYA"

# Predetermined prompt (replace with your desired prompt)
PROMPT = "Write a short description of this image."

def get_user_image(image_path):
    """Opens the image at the given path."""
    try:
        image = Image.open(image_path)
        return image
    except FileNotFoundError:
        print("Error: File not found. Please try again.")
        return None

def call_gemini(image, prompt):
    """Configures API and sends a request with both image and prompt."""
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro-vision")

    # Send request with both text and image
    response = model.generate_content([prompt, image], stream=True)
    response.resolve()
    return response.text

def main():
    """Gets user image from command line argument, calls Gemini, and prints response to a file."""
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    image = get_user_image(image_path)
    if image:
        answer = call_gemini(image, PROMPT)

        output_filename = f"{image.filename}.gemini.output"
        with open(output_filename, "w") as output_file:
            output_file.write(answer)

        print(f"Output written to {output_filename}")
    else:
        print("Couldn't get your image. Please try again.")

if __name__ == "__main__":
    main()
