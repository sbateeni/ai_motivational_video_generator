from flask import Flask, render_template, jsonify
from datetime import datetime
import os
from dotenv import load_dotenv

from utils.text_generator import generate_motivational_quote
from utils.video_generator import generate_video
from utils.video_editor import add_text_to_video
from utils.youtube_uploader import upload_to_youtube
from utils.logger import logger

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_daily_video():
    """Generate and upload a daily motivational video."""
    try:
        # Generate quote
        quote = generate_motivational_quote()
        logger.info(f"Generated quote: {quote}")
        
        # Generate video
        video_path = generate_video()
        logger.info(f"Generated video at: {video_path}")
        
        # Add text to video
        final_video_path = add_text_to_video(video_path, quote)
        logger.info(f"Added text to video. Final video at: {final_video_path}")
        
        # Upload to YouTube
        title = f"رحلة اليوم – اقتباس من العظماء ({datetime.now().strftime('%Y-%m-%d')})"
        description = f"اقتباس اليوم: {quote}\n\nتابعونا للمزيد من المحتوى التحفيزي!"
        
        upload_result = upload_to_youtube(final_video_path, title, description)
        logger.info(f"Uploaded to YouTube. Video ID: {upload_result['id']}")
        
        # Clean up temporary files
        os.remove(video_path)
        os.remove(final_video_path)
        logger.info("Cleaned up temporary files")
        
        return jsonify({
            'success': True,
            'message': 'Video generated and uploaded successfully',
            'video_id': upload_result['id']
        })
    
    except Exception as e:
        logger.error(f"Error in generate_daily_video: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Check the health of the application."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 