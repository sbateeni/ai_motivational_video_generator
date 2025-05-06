from setuptools import setup, find_packages

setup(
    name="ai_motivational_video_generator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.32.0",
        "python-dotenv==1.0.1",
        "google-generativeai==0.3.2",
        "numpy==1.26.4",
        "moviepy==1.0.3",
        "opencv-python-headless==4.9.0.80",
        "Pillow==10.2.0",
        "gTTS==2.5.1",
        "pydub==0.25.1",
        "requests==2.31.0"
    ]
) 