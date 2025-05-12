import os
import google.generativeai as genai
from dotenv import load_dotenv
from .logger import logger, log_quote

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def setup_gemini():
    """Setup Google Gemini API."""
    genai.configure(api_key=GOOGLE_API_KEY)
    return genai.GenerativeModel('models/gemini-2.0-flash-001')

def generate_motivational_quote():
    """Generate a motivational quote using Google Gemini."""
    try:
        model = setup_gemini()
        prompt = """
        Generate a short, powerful motivational quote from famous authors or leaders.
        The quote should be:
        - Under 100 characters
        - Inspiring and meaningful
        - From a well-known figure
        - In a clear, concise language
        """
        
        response = model.generate_content(prompt)
        quote = response.text.strip()
        
        # Log the generated quote
        log_quote(quote)
        logger.info(f"Generated quote: {quote}")
        
        return quote
    
    except Exception as e:
        logger.error(f"Error generating quote: {str(e)}")
        raise 