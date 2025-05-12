import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from .logger import logger

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_DIR = BASE_DIR / 'credentials'
CLIENT_SECRETS_FILE = CREDENTIALS_DIR / 'client_secrets.json'
TOKEN_FILE = CREDENTIALS_DIR / 'token.json'

# YouTube API setup
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    """Get authenticated YouTube API service."""
    credentials = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # Refresh token if expired
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    
    # Get new token if needed
    if not credentials:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        
        # Save token
        with open(TOKEN_FILE, 'w') as token:
            token.write(credentials.to_json())
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_to_youtube(video_path, title, description):
    """Upload video to YouTube."""
    try:
        youtube = get_authenticated_service()
        
        # Prepare video upload
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['motivation', 'inspiration', 'daily quote'],
                'categoryId': '22'  # People & Blogs
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload video
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True
        )
        
        # Execute upload
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = request.execute()
        logger.info(f"Video uploaded successfully. Video ID: {response['id']}")
        return response
    
    except Exception as e:
        logger.error(f"Error uploading to YouTube: {str(e)}")
        raise 