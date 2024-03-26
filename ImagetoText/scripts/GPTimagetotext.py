import base64
import requests
import sys
import os

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main(image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give me a short description of this image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 100
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()

    # Extract the content portion of the output
    content = response_json['choices'][0]['message']['content']

    # Construct the output file name
    base_name = os.path.splitext(image_path)[0]
    output_file_path = f"{base_name}.GPTdesc.output"

    # Write the content to the output file
    with open(output_file_path, 'w') as file:
        file.write(content)

    # Print a message indicating success
    print(f"Description written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <image_file>")
        sys.exit(1)

    main(sys.argv[1])
