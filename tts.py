# tts.py

from pathlib import Path
from openai import OpenAI
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure this environment variable is set

def read_paragraph(file_path="output/texts/did_you_know.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        paragraph = f.read().strip()
    return paragraph

def generate_audio(paragraph, output_path="output/audio/did_you_know.mp3"):
    CLIENT = OpenAI(api_key=OPENAI_API_KEY)
    speech_file_path = Path(output_path)
    response = CLIENT.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=paragraph
    )
    response.stream_to_file(speech_file_path)
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    paragraph = read_paragraph()
    generate_audio(paragraph)
