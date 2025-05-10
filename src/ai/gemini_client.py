"""
Gemini API client for text generation.
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Missing GEMINI_API_KEY in .env file")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.0-flash"
        
    def generate_content(self, prompt, max_tokens=150):
        """
        Generate content using Gemini API.
        
        Args:
            prompt (str): The prompt to generate content from
            max_tokens (int): Maximum number of tokens to generate
            
        Returns:
            str: Generated content
        """
        url = f"{self.base_url}/{self.model}:generateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        params = {
            "key": self.api_key
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.7,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        try:
            response = requests.post(url, headers=headers, params=params, json=data)
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return content.strip()
            else:
                raise ValueError("No content generated")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
            
    def generate_motivational_quote(self, theme):
        """
        Generate a motivational quote using Gemini API.
        
        Args:
            theme (str): The theme for the quote
            
        Returns:
            str: Generated motivational quote
        """
        prompt = f"Generate a short, powerful motivational quote about {theme}. Keep it under 100 characters and make it impactful."
        return self.generate_content(prompt, max_tokens=100) 