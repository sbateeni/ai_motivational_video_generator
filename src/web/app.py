"""
Web interface for the AI Motivational Video Generator.
"""
from flask import Flask, render_template, request, jsonify, send_file
from src.ai.text_generator import TextGenerator
from src.video.video_generator import VideoGenerator
from src.audio.audio_processor import AudioProcessor
import os

app = Flask(__name__)
text_generator = TextGenerator()
video_generator = VideoGenerator()
audio_processor = AudioProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        data = request.json
        theme = data.get('theme')
        
        # Generate motivational quote
        quote = text_generator.generate_motivational_quote(theme)
        
        # Convert text to speech
        speech_path = audio_processor.text_to_speech(quote)
        
        # Mix with background music (if provided)
        music_path = data.get('music_path')
        if music_path:
            mixed_audio_path = audio_processor.mix_audio(
                speech_path,
                music_path,
                'temp_audio/mixed.mp3'
            )
        else:
            mixed_audio_path = speech_path
        
        # Generate video
        background_path = data.get('background_path')
        output_path = video_generator.create_video(
            quote,
            background_path,
            'output/video.mp4'
        )
        
        return jsonify({
            'success': True,
            'quote': quote,
            'video_path': output_path
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    app.run(debug=True) 