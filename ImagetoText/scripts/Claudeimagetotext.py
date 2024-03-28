import requests
import argparse

# Set your API key here
API_KEY = "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"

# The endpoint for the Claude API
API_ENDPOINT = "https://api.claude.openai.com/v1/"

def upload_picture_and_prompt(image_path, prompt):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Prepare the multipart/form-data request
        files = {"image": image_file}
        data = {"prompt": prompt}

        # Set the headers, including the authorization with your API key
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "multipart/form-data"
        }

        # Send the POST request to the Claude API
        response = requests.post(API_ENDPOINT, headers=headers, files=files, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            print("Upload successful!")
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return response.text

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Upload an image and a prompt to the Claude API.")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("prompt", help="Prompt for the image")
    return parser.parse_args()

# Example usage
if __name__ == "__main__":
    args = parse_arguments()
    result = upload_picture_and_prompt(args.image_path, args.prompt)
    print(result)
