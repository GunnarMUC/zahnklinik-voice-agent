# Zahnklinik Voice Agent

Lokaler Echtzeit-Sprach-Assistent für Zahnkliniken mit LiveKit Agents SDK.

## Stack

| Komponente | Technologie |
|------------|-------------|
| Framework | LiveKit Agents SDK (Python) |
| STT (Hören) | Faster-Whisper (lokal) |
| LLM (Denken) | Ollama mit llama3.1 (lokal) |
| TTS (Sprechen) | Piper (lokal) |

## Voraussetzungen

- **Python 3.10+**
- **Ollama** mit Modell `llama3.1`
- **Piper TTS Server** (deutsche Stimme empfohlen)
- **LiveKit** Account (für dev/start)

## Installation

```bash
# Mit uv (empfohlen)
uv venv --python 3.12
uv pip install -r requirements.txt

# Oder mit pip
pip install -r requirements.txt
```

## Konfiguration

Kopiere `.env.example` nach `.env.local` und trage die Werte ein:

```bash
cp .env.example .env.local
```

| Variable | Beschreibung |
|----------|--------------|
| `LIVEKIT_URL` | LiveKit Server URL (z.B. wss://xxx.livekit.cloud) |
| `LIVEKIT_API_KEY` | LiveKit API Key |
| `LIVEKIT_API_SECRET` | LiveKit API Secret |
| `PIPER_URL` | Piper TTS Server (Standard: http://localhost:5000/) |
| `OLLAMA_BASE_URL` | Ollama API (Standard: http://localhost:11434/v1) |
| `OLLAMA_MODEL` | Ollama Modell (Standard: llama3.1) |
| `WHISPER_MODEL` | Faster-Whisper Modell (base, small, medium) |
| `WHISPER_LANGUAGE` | STT-Sprache (Standard: de) |

## Dienste starten

### Ollama
```bash
ollama run llama3.1
```

### Piper TTS (mit deutscher Stimme)
```bash
# Piper installieren
pip install piper-tts[http]

# Deutsche Stimme herunterladen
python3 -m piper.download_voices de_DE-thorsten-medium

# Server starten
python3 -m piper.http_server -m de_DE-thorsten-medium
```

## Ausführung

```bash
# Modelle herunterladen (Silero VAD, Turn Detector)
uv run agent.py download-files

# Console-Modus (Terminal, ohne LiveKit)
uv run agent.py console

# Dev-Modus (mit LiveKit, für Frontend/Playground)
uv run agent.py dev

# Produktion
uv run agent.py start
```

## Features

- **Chat-Kontext:** Merkt sich den Patientennamen über `store_patient_name`
- **Termin-Tools (Platzhalter):**
  - `check_appointment_availability` – Terminverfügbarkeit prüfen
  - `book_appointment` – Termin buchen
  - `cancel_appointment` – Termin stornieren

## Projektstruktur

```
lnm/
├── agent.py          # Haupt-Agent
├── whisper_stt.py    # Faster-Whisper STT-Adapter
├── config.py         # Konfiguration
├── requirements.txt
├── pyproject.toml
└── .env.local        # Credentials (nicht committen)
```
