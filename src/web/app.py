"""
Flask application for generating motivational videos.
"""
import os
import sys
from pathlib import Path
from flask import Flask, request, render_template, send_file, jsonify

# Get the project root directory and add it to Python path
project_root = Path(__file__).parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.ai.text_generator import TextGenerator
from src.video.video_generator import VideoGenerator
from src.audio.audio_processor import AudioProcessor

# Configure Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(project_root, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(project_root, 'output')
app.config['TEMP_FOLDER'] = os.path.join(project_root, 'temp')

# Create necessary directories
for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'], app.config['TEMP_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Initialize components
text_generator = TextGenerator()
video_generator = VideoGenerator()
audio_processor = AudioProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        # Get form data
        background = request.files.get('background')
        audio = request.files.get('audio')
        theme = request.form.get('theme', 'motivation')
        custom_text = request.form.get('customText', '').strip()
        
        # Generate or use custom text
        if custom_text:
            text = custom_text
        else:
            text = text_generator.generate_motivational_quote(theme)
        
        # Save background if provided
        background_path = None
        if background:
            background_path = os.path.join(app.config['UPLOAD_FOLDER'], 'background.jpg')
            background.save(background_path)
        
        # Generate video
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'video.mp4')
        video_path = video_generator.create_video(text, background_path, output_path)
        
        # Add audio if provided
        if audio:
            audio_path = os.path.join(app.config['TEMP_FOLDER'], 'audio.mp3')
            audio.save(audio_path)
            final_path = os.path.join(app.config['OUTPUT_FOLDER'], 'final_video.mp4')
            audio_processor.add_audio_to_video(video_path, audio_path, final_path)
            video_path = final_path
        
        return jsonify({
            'success': True,
            'message': 'Video generated successfully',
            'video_path': video_path
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/video/<path:filename>')
def serve_video(filename):
    try:
        return send_file(
            os.path.join(app.config['OUTPUT_FOLDER'], filename),
            mimetype='video/mp4'
        )
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True) 