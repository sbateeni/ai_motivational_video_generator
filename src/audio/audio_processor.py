"""
Audio processing module for handling voice and music.
"""
from gtts import gTTS
from pydub import AudioSegment
import os

class AudioProcessor:
    def __init__(self):
        self.temp_dir = "temp_audio"
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def text_to_speech(self, text, language='en', output_path=None):
        """
        Convert text to speech using gTTS.
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code (default: 'en')
            output_path (str, optional): Path to save the audio file
            
        Returns:
            str: Path to the generated audio file
        """
        if output_path is None:
            output_path = os.path.join(self.temp_dir, "speech.mp3")
            
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_path)
        return output_path
    
    def mix_audio(self, speech_path, music_path, output_path, music_volume=-20):
        """
        Mix speech with background music.
        
        Args:
            speech_path (str): Path to speech audio file
            music_path (str): Path to background music file
            output_path (str): Path to save the mixed audio
            music_volume (int): Volume of background music in dB
            
        Returns:
            str: Path to the mixed audio file
        """
        # Load audio files
        speech = AudioSegment.from_mp3(speech_path)
        music = AudioSegment.from_mp3(music_path)
        
        # Adjust music volume
        music = music + music_volume
        
        # Loop music if it's shorter than speech
        if len(music) < len(speech):
            music = music * (len(speech) // len(music) + 1)
        
        # Trim music to match speech length
        music = music[:len(speech)]
        
        # Mix audio
        mixed = speech.overlay(music)
        
        # Export
        mixed.export(output_path, format="mp3")
        return output_path 