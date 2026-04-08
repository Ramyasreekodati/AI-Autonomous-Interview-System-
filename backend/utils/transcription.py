import whisper
import os
import logging
import torch

logger = logging.getLogger(__name__)

class AudioTranscriber:
    """
    Phase 5.1 - Speech-to-Text & Voice Analysis
    Uses OpenAI Whisper to transcribe interview audio responses.
    """
    def __init__(self, model_size="base"):
        logger.info(f"Initializing Whisper model: {model_size}")
        try:
            # Check for GPU
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = whisper.load_model(model_size, device=device)
            self.enabled = True
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.enabled = False

    def transcribe(self, audio_path):
        """
        Transcribes audio file to text.
        """
        if not self.enabled or not os.path.exists(audio_path):
            return "Transcription unavailable (Model load failed or file missing)."
        
        try:
            result = self.model.transcribe(audio_path)
            return result.get("text", "").strip()
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return f"Error during transcription: {str(e)}"

# Singleton instance
transcriber = AudioTranscriber()
