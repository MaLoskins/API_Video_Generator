# main.py

import subprocess
import sys
import os
import glob
import shutil
from moviepy.editor import AudioFileClip, ImageSequenceClip

def run_script(script_name, args=None):
    try:
        cmd = [sys.executable, script_name]
        if args:
            cmd.extend(args)
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_name}: {e}")
        sys.exit(1)

def get_unique_output_path(base_path):
    """
    Generates a unique file path by appending a number if the base_path already exists.
    Example: if did_you_know.mp4 exists, it returns did_you_know1.mp4, then did_you_know2.mp4, etc.
    """
    if not os.path.exists(base_path):
        return base_path
    base, ext = os.path.splitext(base_path)
    counter = 1
    while True:
        new_path = f"{base}{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def create_video(audio_path, images_dir, output_path, fps=24):
    # Check if audio file exists
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Get list of image files sorted alphabetically
    image_files = sorted(glob.glob(os.path.join(images_dir, "*.png")))
    
    if not image_files:
        raise FileNotFoundError(f"No PNG images found in directory: {images_dir}")
    
    # Load audio and get its duration
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration  # duration in seconds
    
    print(f"Audio Duration: {audio_duration:.2f} seconds")
    print(f"Number of Images: {len(image_files)}")
    
    # Calculate duration per image
    duration_per_image = audio_duration / len(image_files)
    print(f"Duration per image: {duration_per_image:.2f} seconds")
    
    # Create a list of durations for each image
    durations = [duration_per_image] * len(image_files)
    
    # Create ImageSequenceClip with specified durations
    video_clip = ImageSequenceClip(image_files, durations=durations)
    
    # Ensure the video duration matches the audio duration
    video_clip = video_clip.set_duration(audio_duration)
    
    # Set the audio to the video clip
    video_clip = video_clip.set_audio(audio_clip)
    
    # Write the final video to a file with specified fps and codecs
    video_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=fps,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        verbose=True,
        logger='bar'
    )
    
    # Close clips to release resources
    audio_clip.close()
    video_clip.close()

def clear_directory(dir_path):
    """
    Removes all files and subdirectories in the specified directory.
    """
    if not os.path.isdir(dir_path):
        print(f"Directory does not exist: {dir_path}")
        return
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def main(topic):
    # Ensure output directories exist
    os.makedirs("output/texts", exist_ok=True)
    os.makedirs("output/images", exist_ok=True)
    os.makedirs("output/audio", exist_ok=True)
    os.makedirs("output/video", exist_ok=True)  # Ensure video directory exists
    
    print("Starting Text Generation...")
    run_script("text_generation.py", args=[topic])
    
    print("\nStarting Image Generation...")
    run_script("image_generation.py")
    
    print("\nStarting Text-to-Speech Conversion...")
    run_script("tts.py")
    
    print("\nAll processes completed successfully!")
    
    # Define paths
    AUDIO_PATH = "output/audio/did_you_know.mp3"
    IMAGES_DIR = "output/images"
    BASE_OUTPUT_VIDEO = "output/video/did_you_know.mp4"
    
    # Get a unique output video path to prevent overwriting
    OUTPUT_VIDEO = get_unique_output_path(BASE_OUTPUT_VIDEO)
    
    # Create the video
    print(f"\nCreating video at {OUTPUT_VIDEO}...")
    create_video(AUDIO_PATH, IMAGES_DIR, OUTPUT_VIDEO)
    
    print(f"Video created successfully at {OUTPUT_VIDEO}")
    
    # Clean up directories after video creation
    print("\nCleaning up temporary files...")
    clear_directory("output/texts")
    clear_directory("output/images")
    clear_directory("output/audio")
    print("Cleanup completed successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <topic>")
        sys.exit(1)
    topic = sys.argv[1]
    main(topic)
