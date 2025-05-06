"""
Web interface for the AI Motivational Video Generator.
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.ai.text_generator import TextGenerator
from src.video.video_generator import VideoGenerator
from src.audio.audio_processor import AudioProcessor
import tempfile

# Initialize components
text_generator = TextGenerator()
video_generator = VideoGenerator()
audio_processor = AudioProcessor()

# Set page config
st.set_page_config(
    page_title="AI Motivational Video Generator",
    page_icon="🎥",
    layout="wide"
)

@st.cache
def generate_video(theme):
    try:
        # Generate motivational quote
        quote = text_generator.generate_motivational_quote(theme)
        
        # Convert text to speech
        speech_path = audio_processor.text_to_speech(quote)
        
        # Mix with background music (if provided)
        music_path = st.session_state.music_path
        if music_path:
            mixed_audio_path = audio_processor.mix_audio(
                speech_path,
                music_path,
                'temp_audio/mixed.mp3'
            )
        else:
            mixed_audio_path = speech_path
        
        # Generate video
        background_path = st.session_state.background_path
        output_path = video_generator.create_video(
            quote,
            background_path,
            'output/video.mp4'
        )
        
        return {
            'success': True,
            'quote': quote,
            'video_path': output_path
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    st.title("AI Motivational Video Generator")

    # File uploaders
    uploaded_file = st.file_uploader("Choose a background image", type=["jpg", "png"])
    if uploaded_file:
        st.session_state.background_path = uploaded_file.name

    uploaded_music = st.file_uploader("Choose a background music", type=["mp3"])
    if uploaded_music:
        st.session_state.music_path = uploaded_music.name

    # Generate button
    if st.button("Generate Video"):
        if 'background_path' in st.session_state and 'music_path' in st.session_state:
            result = generate_video(st.session_state.theme)
            if result['success']:
                st.success("Video generated successfully!")
                st.write("Quote:")
                st.write(result['quote'])
                st.write("Video Path:")
                st.write(result['video_path'])
            else:
                st.error(f"Error: {result['error']}")
        else:
            st.error("Please upload both background image and music.")

    # Rest of the component
    st.write("This is a Streamlit app for generating motivational videos.")

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    main() 