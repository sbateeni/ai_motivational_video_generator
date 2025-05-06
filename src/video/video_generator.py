"""
Enhanced video generation module using MoviePy with dynamic animations and effects.
Optimized for short, high-quality videos.
"""
import sys
import os
from pathlib import Path
from moviepy.config import change_settings
from moviepy.editor import (
    VideoFileClip, TextClip, CompositeVideoClip, ImageClip, ColorClip,
    concatenate_videoclips, vfx, transfx
)
import random
import numpy as np

# Configure MoviePy to use ImageMagick
if sys.platform.startswith('win'):
    # Use the installed ImageMagick path
    magick_path = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
    if os.path.exists(magick_path):
        change_settings({"IMAGEMAGICK_BINARY": magick_path})
        print(f"Using ImageMagick from: {magick_path}")
    else:
        print("Warning: ImageMagick not found. Please verify the installation path.")

class VideoGenerator:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.duration = 15  # Default duration in seconds for YouTube shorts
        self.fps = 30  # Higher FPS for smoother animations
        
        # Define text styles optimized for YouTube
        self.text_styles = [
            {
                'fontsize': 90,
                'color': '#FFFFFF',
                'font': 'Arial-Bold',
                'stroke_color': '#000000',
                'stroke_width': 3,
                'shadow': True
            },
            {
                'fontsize': 85,
                'color': '#FFD700',
                'font': 'Arial-Bold',
                'stroke_color': '#000000',
                'stroke_width': 3,
                'shadow': True
            },
            {
                'fontsize': 95,
                'color': '#00FF00',
                'font': 'Arial-Bold',
                'stroke_color': '#000000',
                'stroke_width': 3,
                'shadow': True
            }
        ]
        
        # Define transitions optimized for short videos
        self.transitions = [
            transfx.crossfadein,
            transfx.crossfadeout,
            transfx.slide_in,
            transfx.slide_out
        ]
        
    def create_text_clip(self, text, duration=None, style=None):
        """
        Create a text clip with the given text and style.
        Optimized for YouTube shorts.
        
        Args:
            text (str): The text to display
            duration (float, optional): Duration of the clip in seconds
            style (dict, optional): Text style dictionary
            
        Returns:
            TextClip: The created text clip
        """
        try:
            # Select random style if none provided
            if style is None:
                style = random.choice(self.text_styles)
            
            # Create base text clip
            text_clip = TextClip(
                text,
                fontsize=style['fontsize'],
                color=style['color'],
                font=style['font'],
                size=(self.width * 0.9, None),
                method='label',
                stroke_color=style['stroke_color'],
                stroke_width=style['stroke_width']
            ).set_duration(duration or self.duration)
            
            # Add dynamic animations
            def position_animation(t):
                # Smooth floating effect
                x_offset = 15 * np.sin(t * 3)
                y_offset = 10 * np.cos(t * 2)
                return ('center', 'center')
            
            # Add scale animation
            def scale_animation(t):
                # Subtle pulsing effect
                scale = 1 + 0.05 * np.sin(t * 4)
                return scale
            
            # Apply animations
            text_clip = text_clip.set_position(position_animation)
            text_clip = text_clip.resize(scale_animation)
            
            # Add fade effects
            text_clip = text_clip.fadein(0.3).fadeout(0.3)
            
            return text_clip
        except Exception as e:
            print(f"Error creating text clip: {str(e)}")
            raise
    
    def create_background(self, background_path=None):
        """
        Create a dynamic background clip with effects.
        Optimized for YouTube shorts.
        
        Args:
            background_path (str, optional): Path to background image/video
            
        Returns:
            VideoClip: The background clip
        """
        try:
            if background_path and os.path.exists(background_path):
                # Load and process background
                if background_path.endswith(('.mp4', '.avi', '.mov')):
                    background = VideoFileClip(background_path)
                else:
                    background = ImageClip(background_path)
                
                # Resize background to match dimensions
                background = background.resize((self.width, self.height))
                background = background.set_duration(self.duration)
                
                # Add dynamic effects
                background = background.fx(vfx.colorx, 1.2)  # Enhance colors
                background = background.fx(vfx.lum_contrast, lum=1.1, contrast=1.1)  # Enhance contrast
                
                # Add subtle zoom effect
                def zoom_effect(t):
                    return 1 + 0.1 * np.sin(t * 2)
                
                background = background.resize(zoom_effect)
            else:
                # Create dynamic gradient background
                def make_frame(t):
                    # Create a dynamic gradient
                    gradient = np.zeros((self.height, self.width, 3))
                    for i in range(self.height):
                        # Dynamic color based on time
                        r = 0.1 + 0.1 * np.sin(t + i/self.height * np.pi)
                        g = 0.1 + 0.1 * np.sin(t * 1.5 + i/self.height * np.pi)
                        b = 0.2 + 0.1 * np.sin(t * 2 + i/self.height * np.pi)
                        gradient[i, :] = [r, g, b]
                    return gradient
                
                background = VideoFileClip(None, ismask=False, duration=self.duration)
                background = background.set_make_frame(make_frame)
            
            return background
        except Exception as e:
            print(f"Error creating background: {str(e)}")
            raise
    
    def create_video(self, text, background_path=None, output_path='output.mp4'):
        """
        Create a dynamic video optimized for YouTube shorts.
        
        Args:
            text (str): The text to display
            background_path (str, optional): Path to background image/video
            output_path (str): Path to save the output video
            
        Returns:
            str: Path to the created video
        """
        try:
            # Ensure output path is absolute
            output_path = os.path.abspath(output_path)
            
            # Split text into sentences for multiple scenes
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            # Calculate duration per scene
            scene_duration = min(3, self.duration / len(sentences))
            
            # Create clips for each sentence
            clips = []
            for i, sentence in enumerate(sentences):
                # Create background for this scene
                background = self.create_background(background_path)
                
                # Create text clip with random style
                text_clip = self.create_text_clip(sentence, duration=scene_duration)
                
                # Combine background and text
                scene = CompositeVideoClip([background, text_clip])
                
                # Add transition effects
                if i > 0:
                    scene = scene.set_start(i * scene_duration)
                    scene = scene.crossfadein(0.3)
                
                clips.append(scene)
            
            # Concatenate all clips
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Write the result to a file with high quality settings
            final_clip.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio=False,
                threads=4,
                preset='slow',  # Higher quality encoding
                bitrate='8000k'  # High bitrate for better quality
            )
            
            # Close the clip to free up resources
            final_clip.close()
            
            return output_path
        except Exception as e:
            print(f"Error creating video: {str(e)}")
            raise 