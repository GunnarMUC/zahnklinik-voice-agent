"""
Zentrale Konfiguration für den Zahnklinik Voice Agent.
Alle Werte können über Umgebungsvariablen überschrieben werden.
"""

import os

from dotenv import load_dotenv

load_dotenv(".env.local")

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
