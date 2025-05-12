import os
from datetime import datetime
from flask import Flask, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import requests
import json
import pickle

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# YouTube API configuration
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = "client_secrets.json"

def get_youtube_credentials():
    """Get YouTube API credentials."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def generate_motivational_quote():
    """Generate a motivational quote using Google Gemini."""
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Generate a short, powerful motivational quote from famous authors or leaders. Keep it under 100 characters."
    response = model.generate_content(prompt)
    return response.text.strip()

def create_video_with_text(video_path, text):
    """Create a video with text overlay."""
    video = VideoFileClip(video_path)
    
    # Create text clip
    txt_clip = TextClip(text, fontsize=70, color='white', font='Arial-Bold')
    txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(video.duration)
    
    # Composite video
    final_video = CompositeVideoClip([video, txt_clip])
    
    # Generate output filename
    output_filename = f"video_{datetime.now().strftime('%Y%m%d')}.mp4"
    final_video.write_videofile(output_filename)
    
    return output_filename

def upload_to_youtube(video_path, title, description):
    """Upload video to YouTube."""
    credentials = get_youtube_credentials()
    youtube = build('youtube', 'v3', credentials=credentials)
    
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['motivation', 'inspiration', 'daily quote'],
            'categoryId': '22'  # People & Blogs category
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    mediaFile = youtube.media().upload(
        part='snippet,status',
        body=request_body,
        media_body=video_path,
        media_mime_type='video/mp4'
    )
    
    return mediaFile.execute()

@app.route('/generate', methods=['POST'])
def generate_video():
    try:
        # Generate quote
        quote = generate_motivational_quote()
        
        # Create video with text
        video_path = create_video_with_text('base_video.mp4', quote)
        
        # Upload to YouTube
        title = f"رحلة اليوم – اقتباس من العظماء ({datetime.now().strftime('%Y-%m-%d')})"
        description = f"اقتباس اليوم: {quote}\n\nتابعونا للمزيد من المحتوى التحفيزي!"
        
        upload_result = upload_to_youtube(video_path, title, description)
        
        return jsonify({
            'success': True,
            'message': 'Video generated and uploaded successfully',
            'video_id': upload_result['id']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 