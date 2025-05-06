"""
Text generation module for motivational quotes.
"""
import random

class TextGenerator:
    def __init__(self):
        self.quotes = [
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "The only way to do great work is to love what you do.",
            "Believe you can and you're halfway there.",
            "Everything you've ever wanted is on the other side of fear.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "Don't watch the clock; do what it does. Keep going.",
            "The only limit to our realization of tomorrow will be our doubts of today.",
            "Success is walking from failure to failure with no loss of enthusiasm.",
            "The way to get started is to quit talking and begin doing.",
            "Your time is limited, don't waste it living someone else's life."
        ]
    
    def generate_motivational_quote(self, theme=None):
        """
        Generate a motivational quote.
        
        Args:
            theme (str, optional): Theme for the quote (not used in this simple version)
            
        Returns:
            str: A motivational quote
        """
        try:
            return random.choice(self.quotes)
        except Exception as e:
            print(f"Error generating quote: {str(e)}")
            raise 