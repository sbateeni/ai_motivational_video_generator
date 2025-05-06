import sys
import os

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

try:
    import moviepy
    print(f"MoviePy version: {moviepy.__version__}")
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip, ColorClip
    print("Successfully imported all MoviePy components")
except ImportError as e:
    print(f"Error importing moviepy: {e}")
    print(f"Current working directory: {os.getcwd()}")
    raise 