"""
Audio processing module for text-to-speech and audio mixing.
"""
import os
from gtts import gTTS
import tempfile
from moviepy.editor import VideoFileClip, AudioFileClip

class AudioProcessor:
    def __init__(self):
        self.temp_dir = 'temp_audio'
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def text_to_speech(self, text):
        """
        Convert text to speech using gTTS.
        
        Args:
            text (str): Text to convert to speech
            
        Returns:
            str: Path to the generated audio file
        """
        try:
            # Create a temporary file for the speech
            speech_path = os.path.join(self.temp_dir, 'speech.mp3')
            
            # Generate speech using gTTS
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(speech_path)
            
            return speech_path
        except Exception as e:
            print(f"Error in text_to_speech: {str(e)}")
            raise
    
    def mix_audio(self, speech_path, music_path, output_path):
        """
        Mix speech with background music.
        For now, we'll just return the speech path as we're having issues with pydub.
        
        Args:
            speech_path (str): Path to the speech audio file
            music_path (str): Path to the background music file
            output_path (str): Path to save the mixed audio
            
        Returns:
            str: Path to the mixed audio file
        """
        try:
            # For now, just return the speech path
            # In a production environment, you would want to properly mix the audio
            return speech_path
        except Exception as e:
            print(f"Error in mix_audio: {str(e)}")
            raise

    def add_audio_to_video(self, video_path, audio_path, output_path):
        """
        Add audio to a video file.
        
        Args:
            video_path (str): Path to the video file
            audio_path (str): Path to the audio file
            output_path (str): Path to save the final video
            
        Returns:
            str: Path to the final video file
        """
        try:
            # Load the video and audio
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            # Set the audio duration to match the video
            audio = audio.set_duration(video.duration)
            
            # Add the audio to the video
            final_video = video.set_audio(audio)
            
            # Write the result to a file
            final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            
            # Close the clips to free up resources
            video.close()
            audio.close()
            final_video.close()
            
            return output_path
        except Exception as e:
            print(f"Error in add_audio_to_video: {str(e)}")
            raise 