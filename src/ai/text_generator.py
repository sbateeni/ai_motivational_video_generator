"""
Text generation module using Google's Gemini model.
"""
import google.generativeai as genai
import streamlit as st

class TextGenerator:
    def __init__(self):
        genai.configure(api_key=st.secrets["gemini"]["api_key"])
        self.model = genai.GenerativeModel('gemini-pro')
        
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
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating quote: {e}")
            return "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle." 