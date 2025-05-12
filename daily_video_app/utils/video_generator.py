import os
import torch
from pathlib import Path
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
from .logger import logger

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
VIDEOS_DIR = DATA_DIR / 'videos'

def generate_video():
    """Generate a video using Hugging Face model."""
    try:
        # Create videos directory if it doesn't exist
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Initialize the pipeline
        pipe = DiffusionPipeline.from_pretrained(
            "damo-vilab/text-to-video-ms-1.7b",
            torch_dtype=torch.float16,
            variant="fp16"
        )
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        
        # Optimize for GPU memory
        pipe.enable_model_cpu_offload()
        pipe.enable_vae_slicing()
        
        # Generate video
        prompt = "A sleek car driving through lush green mountains at sunrise, cinematic quality, 4k"
        video_frames = pipe(
            prompt,
            num_inference_steps=25,
            num_frames=50  # This will generate about 2 seconds of video
        ).frames
        
        # Save video
        output_path = VIDEOS_DIR / f"generated_video_{os.path.basename(prompt[:30])}.mp4"
        video_path = export_to_video(video_frames, str(output_path))
        
        logger.info(f"Generated video at: {video_path}")
        return video_path
    
    except Exception as e:
        logger.error(f"Error generating video: {str(e)}")
        raise 