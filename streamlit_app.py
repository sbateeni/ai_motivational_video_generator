"""
Streamlit Cloud entry point for the AI Motivational Video Generator.
"""
import os
import streamlit as st
from app import *

# Set environment variables for Streamlit Cloud
if 'OPENAI_API_KEY' not in os.environ:
    st.error("Please set your OpenAI API key in the Streamlit Cloud secrets.")
    st.stop() 