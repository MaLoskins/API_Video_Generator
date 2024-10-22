# create_video.py
import os
import glob
from moviepy.editor import AudioFileClip, ImageSequenceClip

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

if __name__ == "__main__":
    # Define paths
    AUDIO_PATH = "output/audio/did_you_know.mp3"
    IMAGES_DIR = "output/images"
    OUTPUT_VIDEO = "output/video/did_you_know.mp4"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)
    
    # Create the video
    create_video(AUDIO_PATH, IMAGES_DIR, OUTPUT_VIDEO)
    
    print(f"Video created successfully at {OUTPUT_VIDEO}")
