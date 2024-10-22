# text_generation.py

import openai
import os
import sys
from openai import OpenAI

# Ensure the OpenAI API key is set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: The environment variable OPENAI_API_KEY is not set.")
    sys.exit(1)

CLIENT = OpenAI(api_key=OPENAI_API_KEY)

def generate_did_you_know(topic):
    prompt = (
        f"Write a paragraph starting with 'Did you know' about {topic} followed by an interesting fact. "
        "The paragraph should be between 60-100 words."
    )
    
    try:
        response = CLIENT.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates interesting facts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        paragraph = response.choices[0].message.content.strip()
        return paragraph
    except Exception as e:
        print(f"Error during ChatCompletion API call: {e}")
        sys.exit(1)

def extract_image_descriptions(paragraph):
    prompt = (
        "Extract the main concepts from the following paragraph and provide them as image descriptions. "
        "Format each description as 'An image of ...' and separate each with '[SEPARATE]'. dont include diagrams or text type images \n\n"
        f"Paragraph: {paragraph}"
    )
    
    try:
        response = CLIENT.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You extract concepts for image descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.5,
        )
        descriptions_text = response.choices[0].message.content.strip()
        # Split the descriptions by '[SEPARATE]' and clean them
        descriptions = [desc.strip() for desc in descriptions_text.split("[SEPARATE]")]
        return descriptions
    except Exception as e:
        print(f"Error during ChatCompletion API call for image descriptions: {e}")
        sys.exit(1)

def save_texts(paragraph, descriptions, output_dir="output/texts"):
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(os.path.join(output_dir, "did_you_know.txt"), "w", encoding="utf-8") as f:
            f.write(paragraph)
        
        with open(os.path.join(output_dir, "image_descriptions.txt"), "w", encoding="utf-8") as f:
            for desc in descriptions:
                f.write(desc + "\n")
    except Exception as e:
        print(f"Error saving text files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    paragraph = generate_did_you_know(sys.argv[1])
    print("Generated Paragraph:")
    print(paragraph)
    
    descriptions = extract_image_descriptions(paragraph)
    print("\nExtracted Image Descriptions:")
    for desc in descriptions:
        print(desc)
    
    save_texts(paragraph, descriptions)
    print("\nTexts saved to output/texts/")
