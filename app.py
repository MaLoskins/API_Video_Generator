# app.py

import streamlit as st
import subprocess
import sys
import os
import glob

def run_main_script(topic):
    """
    Runs the main.py script with the specified topic.
    """
    try:
        # Run main.py with the topic
        result = subprocess.run(
            [sys.executable, "main.py", topic],
            capture_output=True,
            text=True,
            check=True
        )
        return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"success": False, "stdout": e.stdout, "stderr": e.stderr}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e)}

def get_latest_video(video_dir="output/video"):
    """
    Retrieves the latest video file from the specified directory.
    """
    video_files = sorted(
        glob.glob(os.path.join(video_dir, "*.mp4")),
        key=os.path.getmtime
    )
    if video_files:
        return video_files[-1]  # Return the most recently modified video
    else:
        return None

def main():
    st.set_page_config(page_title="Did You Know Video Generator", layout="centered")
    st.title("📹 Did You Know Video Generator")
    st.write("Generate a personalized 'Did You Know' video based on your chosen topic.")

    with st.form("video_generator_form"):
        topic = st.text_input("Enter a general topic:", "")
        submit_button = st.form_submit_button("Generate Video")

    if submit_button:
        if not topic.strip():
            st.error("Please enter a valid topic.")
        else:
            st.info("Generating video. This may take a few minutes...")
            with st.spinner("Processing..."):
                result = run_main_script(topic)
            
            if result["success"]:
                st.success("Video generated successfully!")
                latest_video = get_latest_video()
                if latest_video:
                    st.video(latest_video)
                else:
                    st.error("Video generation succeeded, but no video file was found.")
            else:
                st.error("An error occurred during video generation:")
                st.text(result["stderr"])

    st.markdown("---")
    st.write("### Instructions")
    st.write("""
    1. **Enter a Topic**: Provide a general topic you're interested in.
    2. **Generate Video**: Click the "Generate Video" button to start the process.
    3. **View Video**: Once generated, the video will be displayed below.
    """)

    st.markdown("---")
    st.write("### Technical Details")
    st.write("""
    - **Text Generation**: Creates a 'Did You Know' paragraph based on your topic.
    - **Image Generation**: Generates relevant images.
    - **Text-to-Speech**: Converts the text into audio.
    - **Video Compilation**: Combines audio and images into a video.
    """)

if __name__ == "__main__":
    main()
