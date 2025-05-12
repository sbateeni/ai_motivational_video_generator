import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
VIDEOS_DIR = DATA_DIR / 'videos'
CREDENTIALS_DIR = BASE_DIR / 'credentials'

# API Keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# YouTube API settings
YOUTUBE_CLIENT_SECRETS_FILE = CREDENTIALS_DIR / 'youtube_client_secret.json'
YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Video settings
VIDEO_DURATION = 10  # seconds
VIDEO_FPS = 30
VIDEO_RESOLUTION = (1920, 1080)

# Text settings
FONT_SIZE = 70
FONT_COLOR = 'white'
FONT_NAME = 'Arial-Bold'

# Logging settings
LOG_FILE = DATA_DIR / 'quotes_log.txt'

# Ensure directories exist
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True) 