"""
Zentrale Konfiguration für den Zahnklinik Voice Agent.
Alle Werte können über Umgebungsvariablen überschrieben werden.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env.local")


def _validate_config() -> None:
    """Raise clear errors if required environment variables are missing."""
    missing = []
    for var in ("LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"):
        if not os.getenv(var):
            missing.append(var)
    if missing:
        msg = (
            "Fehlende LiveKit-Umgebungsvariablen: "
            + ", ".join(missing)
            + ". Bitte .env.local prüfen (siehe .env.example)."
        )
        raise ValueError(msg)

# LiveKit (erforderlich für dev/start)
LIVEKIT_URL = os.getenv("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "")

# Ollama LLM
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# Piper TTS (Server muss mit deutscher Stimme gestartet werden, z.B. -m de_DE-thorsten-medium)
PIPER_URL = os.getenv("PIPER_URL", "http://localhost:5000/")

# Faster-Whisper STT
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # base, small, medium, large-v3
WHISPER_LANGUAGE = os.getenv("WHISPER_LANGUAGE", "de")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "auto")  # auto, cpu, cuda
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "float32")  # float32, float16, int8
