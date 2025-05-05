"""
Text generation module using OpenAI's GPT model.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

class TextGenerator:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def generate_motivational_quote(self, theme=None):
        """
        Generate a motivational quote based on an optional theme.
        
        Args:
            theme (str, optional): The theme for the motivational quote.
            
        Returns:
            str: Generated motivational quote
        """
        prompt = f"Generate a short, powerful motivational quote{f' about {theme}' if theme else ''}. Keep it under 100 words."
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a motivational speaker who creates powerful, inspiring quotes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating quote: {e}")
            return "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle." 