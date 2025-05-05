"""
Video generation module using MoviePy.
"""
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, ColorClip
from PIL import Image
import numpy as np

class VideoGenerator:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.duration = 10  # Default duration in seconds
        
    def create_text_clip(self, text, duration=None):
        """
        Create a text clip with the given text.
        
        Args:
            text (str): The text to display
            duration (float, optional): Duration of the clip in seconds
            
        Returns:
            TextClip: The created text clip
        """
        return TextClip(
            text,
            fontsize=70,
            color='white',
            font='Arial-Bold',
            size=(self.width, None),
            method='caption'
        ).set_duration(duration or self.duration)
    
    def create_video(self, text, background_path=None, output_path='output.mp4'):
        """
        Create a video with the given text and optional background.
        
        Args:
            text (str): The text to display
            background_path (str, optional): Path to background image/video
            output_path (str): Path to save the output video
            
        Returns:
            str: Path to the created video
        """
        # Create text clip
        text_clip = self.create_text_clip(text)
        text_clip = text_clip.set_position('center')
        
        if background_path:
            # Load and process background
            if background_path.endswith(('.mp4', '.avi', '.mov')):
                background = VideoFileClip(background_path)
            else:
                background = ImageClip(background_path)
            
            # Resize background to match dimensions
            background = background.resize((self.width, self.height))
            
            # Create final video
            final_clip = CompositeVideoClip([background, text_clip])
        else:
            # Create solid color background
            color_clip = ColorClip(size=(self.width, self.height), color=(0, 0, 0))
            final_clip = CompositeVideoClip([color_clip, text_clip])
        
        # Write the result to a file
        final_clip.write_videofile(output_path, fps=24)
        return output_path 