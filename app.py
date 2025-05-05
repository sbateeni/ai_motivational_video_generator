"""
AI Motivational Video Generator using Streamlit.
"""
import streamlit as st
import os
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

# Title and description
st.title("🎥 AI Motivational Video Generator")
st.markdown("""
Create inspiring motivational videos with AI-generated quotes, custom backgrounds, and background music.
""")

# Create columns for input
col1, col2 = st.columns(2)

with col1:
    # Theme input
    theme = st.text_input("Theme (optional)", placeholder="Enter a theme for your motivational video")
    
    # Background upload
    background_file = st.file_uploader("Background Image/Video (optional)", type=['jpg', 'jpeg', 'png', 'mp4', 'mov'])
    
    # Music upload
    music_file = st.file_uploader("Background Music (optional)", type=['mp3', 'wav'])

# Generate button
if st.button("Generate Video", type="primary"):
    if not theme and not background_file and not music_file:
        st.warning("Please provide at least one input (theme, background, or music)")
    else:
        with st.spinner("Generating your motivational video..."):
            try:
                # Create temporary directory for processing
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Generate quote
                    quote = text_generator.generate_motivational_quote(theme)
                    st.success("Generated Quote:")
                    st.write(quote)
                    
                    # Process background file if provided
                    background_path = None
                    if background_file:
                        background_path = os.path.join(temp_dir, background_file.name)
                        with open(background_path, 'wb') as f:
                            f.write(background_file.getvalue())
                    
                    # Process music file if provided
                    music_path = None
                    if music_file:
                        music_path = os.path.join(temp_dir, music_file.name)
                        with open(music_path, 'wb') as f:
                            f.write(music_file.getvalue())
                    
                    # Generate speech
                    speech_path = audio_processor.text_to_speech(quote)
                    
                    # Mix audio if music provided
                    if music_path:
                        final_audio_path = audio_processor.mix_audio(
                            speech_path,
                            music_path,
                            os.path.join(temp_dir, 'mixed.mp3')
                        )
                    else:
                        final_audio_path = speech_path
                    
                    # Generate video
                    output_path = video_generator.create_video(
                        quote,
                        background_path,
                        os.path.join(temp_dir, 'output.mp4')
                    )
                    
                    # Display video
                    st.video(output_path)
                    
                    # Download button
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label="Download Video",
                            data=f,
                            file_name="motivational_video.mp4",
                            mime="video/mp4"
                        )
                    
            except Exception as e:
                st.error(f"Error generating video: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit") 