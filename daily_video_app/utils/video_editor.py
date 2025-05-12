import os
from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from .logger import logger

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
VIDEOS_DIR = DATA_DIR / 'videos'

def add_text_to_video(video_path, quote):
    """Add text overlay to the video."""
    try:
        # Load video
        video = VideoFileClip(video_path)
        
        # Create text clip
        txt_clip = TextClip(
            quote,
            fontsize=70,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2
        )
        
        # Position text in the center
        txt_clip = txt_clip.set_position('center').set_duration(video.duration)
        
        # Combine video and text
        final_video = CompositeVideoClip([video, txt_clip])
        
        # Save final video
        output_path = VIDEOS_DIR / f"final_video_{os.path.basename(video_path)}"
        final_video.write_videofile(str(output_path))
        
        # Close clips
        video.close()
        final_video.close()
        
        logger.info(f"Added text to video. Final video at: {output_path}")
        return str(output_path)
    
    except Exception as e:
        logger.error(f"Error adding text to video: {str(e)}")
        raise 