# image_generation.py

import os
import requests
from pathlib import Path
from openai import OpenAI

# Set your OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure this environment variable is set

CLIENT = OpenAI(api_key=OPENAI_API_KEY)

def read_image_descriptions(file_path="output/texts/image_descriptions.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        descriptions = [line.strip() for line in f if line.strip()]
    return descriptions

def generate_image(description):
    response = CLIENT.images.generate(
        prompt=description,
        n=1,
        size="512x512",
        response_format="url"
    )
    image_url = response.data[0].url
    return image_url

def download_image(image_url, save_path):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed to download image from {image_url}")

def save_images(descriptions, output_dir="output/images"):
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, desc in enumerate(descriptions, start=1):
        print(f"Generating image {idx}: {desc}")
        image_url = generate_image(desc)
        image_path = os.path.join(output_dir, f"image_{idx}.png")
        download_image(image_url, image_path)
        print(f"Saved image to {image_path}")

if __name__ == "__main__":
    descriptions = read_image_descriptions()
    save_images(descriptions)
    print("\nAll images have been generated and saved to output/images/")
