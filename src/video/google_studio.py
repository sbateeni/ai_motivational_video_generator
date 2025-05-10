"""
Google Studio API integration for video generation.
"""
import os
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# Load environment variables
load_dotenv()

class GoogleStudioAPI:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        self.credentials = None
        self.youtube = None
        
        # Get API credentials from environment variables
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if not all([self.api_key, self.client_id, self.client_secret]):
            raise ValueError("Missing required Google API credentials in .env file")

    def authenticate(self):
        """Authenticate with Google API."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                # Create client config from environment variables
                client_config = {
                    "installed": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": ["http://localhost"]
                    }
                }
                
                flow = InstalledAppFlow.from_client_config(
                    client_config, self.SCOPES)
                self.credentials = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.credentials, token)

        self.youtube = build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            credentials=self.credentials,
            developerKey=self.api_key
        )

    def upload_video(self, video_path, title, description, category_id='22', privacy_status='private'):
        """
        Upload a video to YouTube.
        
        Args:
            video_path (str): Path to the video file
            title (str): Video title
            description (str): Video description
            category_id (str): Video category ID (22 for People & Blogs)
            privacy_status (str): Video privacy status (private, unlisted, public)
            
        Returns:
            dict: Response from YouTube API
        """
        if not self.youtube:
            self.authenticate()

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True
        )

        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = request.execute()
        return response

    def create_short(self, video_path, title, description):
        """
        Create a YouTube Short.
        
        Args:
            video_path (str): Path to the video file
            title (str): Video title
            description (str): Video description
            
        Returns:
            dict: Response from YouTube API
        """
        # Add #shorts to the title and description
        title = f"{title} #shorts"
        description = f"{description}\n\n#shorts"
        
        return self.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            category_id='22',  # People & Blogs
            privacy_status='private'  # Start as private for review
        ) 