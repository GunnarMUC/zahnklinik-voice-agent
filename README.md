# 🦷 Zahnklinik Voice Agent

**Lokaler Echtzeit-Sprachassistent für Zahnarztpraxen** — vollständig offline, datenschutzkonform, deutschsprachig.

Patienten sprechen natürlich, der Agent versteht, antwortet und hilft bei Terminanfragen — ohne dass ein Byte Audio die Praxis verlässt.

---

## Warum dieser Agent?

| Eigenschaft | Zahnklinik Voice Agent | Cloud-basierte Alternativen |
|---|---|---|
| **Sprachverarbeitung** | 100% lokal (Faster-Whisper + Ollama + Piper) | Audio-Daten gehen an Drittanbieter |
| **Datenschutz / DSGVO** | Keine externen API-Calls für STT/LLM/TTS | Patientendaten in US-Clouds |
| **Kosten** | Einmalige Hardware, keine API-Gebühren | Pro-Minute-, Pro-Token-Kosten |
| **Latenz** | Lokal, < 2s Antwortzeit | Netzwerkabhängig |
| **Deutsche Qualität** | Optimiert für Deutsch (STT + TTS) | Oft englisch-zentriert |
| **Kontrollierbarkeit** | Vollständig selbst hostbar | Vendor-Lock-in |

---

## So funktioniert's

```
Patient spricht → Faster-Whisper (STT) → Ollama llama3.1 (LLM) → Piper (TTS) → Antwort
                       ↑                          ↑
                 Silero VAD               Termin-Tools
```

- **Faster-Whisper** transkribiert Sprache auf Deutsch (lokal)
- **Silero VAD** erkennt, wann der Patient zu Ende gesprochen hat
- **Ollama (llama3.1)** versteht die Absicht und entscheidet über die Antwort
- **Piper TTS** generiert eine deutschsprachige Sprachantwort
- **LiveKit Agents** orchestriert den gesamten Echtzeit-Voice-Pipeline

---

## Schnellstart

### Voraussetzungen

- **Python 3.10+** mit [uv](https://docs.astral.sh/uv/)
- **Ollama** installiert, Modell geladen: `ollama pull llama3.1`
- **Piper TTS Server** mit deutscher Stimme: `python3 -m piper.http_server -m de_DE-thorsten-medium`
- **LiveKit** Account (kostenloser Starter-Tier reicht)

### Installation

```bash
git clone https://github.com/GunnarMUC/zahnklinik-voice-agent.git
cd zahnklinik-voice-agent

uv venv --python 3.12
uv pip install -r requirements.txt

cp .env.example .env.local
# LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET in .env.local eintragen

uv run agent.py download-files   # STT/Turn-Detection-Modelle laden
```

### Ausführung

```bash
./run.sh console          # Terminal-Modus (kein LiveKit-Server nötig)
./run.sh dev              # Entwicklungsmodus mit LiveKit
./run.sh start            # Produktionsmodus
./run.sh download-files   # Modelle herunterladen
```

---

## Architektur

```
zahnklinik-voice-agent/
├── agent.py           # ZahnklinikAgent, Tools, AgentSession, CLI-Logik
├── config.py          # Konfiguration via .env.local + Validierung
├── whisper_stt.py     # Faster-Whisper STT-Adapter für LiveKit
├── pyproject.toml     # PEP 621 Projekt-Metadaten + Ruff-Config
├── requirements.txt   # Abhängigkeiten (pip-kompatibel)
├── run.sh             # Start-Skript für alle Modi
├── .env.example       # Vorlage für Umgebungsvariablen
└── README.md          # Diese Datei
```

---

## Konfiguration

Alle Einstellungen via `.env.local` (siehe `.env.example`):

| Variable | Standard | Beschreibung |
|---|---|---|
| `LIVEKIT_URL` | – | LiveKit Server URL (wss://...) |
| `LIVEKIT_API_KEY` | – | LiveKit API Key |
| `LIVEKIT_API_SECRET` | – | LiveKit API Secret |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama API Endpunkt |
| `OLLAMA_MODEL` | `llama3.1` | Verwendetes LLM-Modell |
| `PIPER_URL` | `http://localhost:5000/` | Piper TTS Server |
| `WHISPER_MODEL` | `base` | Faster-Whisper Modellgröße |
| `WHISPER_LANGUAGE` | `de` | Sprache (de = Deutsch) |
| `WHISPER_DEVICE` | `auto` | Device (auto/cpu/cuda) |

---

## Aktueller Status

- [x] Echtzeit-Voice-Pipeline (STT → LLM → TTS)
- [x] Deutsche Sprache optimiert
- [x] Patientennamen-Erkennung (Chat-Kontext)
- [x] Turn Detection (erkennt Sprechende)
- [x] Voice Activity Detection
- [x] Config-Validierung beim Start
- [x] Health-Checks für Ollama und Piper
- [ ] Termin-Tools mit echtem Kalender-Backend
- [ ] Docker-Deployment
- [ ] Unit-Tests
- [ ] Noise Cancellation für Telefonie

---

## Entwicklung

```bash
uv run ruff check .        # Linting
uv run ruff format .       # Auto-Formatierung
```

---

## Lizenz & Kontakt

Projekt von [GunnarMUC](https://github.com/GunnarMUC) — Fragen und Feedback willkommen.
