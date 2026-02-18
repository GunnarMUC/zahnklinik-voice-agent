# Zahnklinik Voice Agent – Projektplan

## Status: Implementiert

Letzte Aktualisierung: 2025-02-18

---

## Übersicht

Lokaler Echtzeit-Sprach-Assistent für Zahnkliniken mit LiveKit Agents SDK.

| Komponente | Technologie | Status |
|------------|-------------|--------|
| Framework | LiveKit Agents SDK (Python) | ✅ |
| STT | Faster-Whisper (lokal) | ✅ |
| LLM | Ollama llama3.1 (lokal) | ✅ |
| TTS | Piper (lokal) | ✅ |
| Chat-Kontext | store_patient_name Tool | ✅ |
| Termin-Tools | Platzhalter | ✅ |

---

## Projektstruktur (aktuell)

```
lnm/
├── agent.py           # Haupt-Agent mit ZahnklinikAgent
├── whisper_stt.py     # Faster-Whisper STT-Adapter
├── config.py          # Zentrale Konfiguration (env)
├── requirements.txt   # Pip-Abhängigkeiten
├── pyproject.toml     # Projekt-Metadaten
├── run.sh             # Start-Skript
├── plan.md            # Dieser Plan
├── README.md          # Dokumentation
├── .env.example       # Env-Vorlage
└── .env.local         # Credentials (gitignore)
```

---

## Konfiguration (Umgebungsvariablen)

| Variable | Beschreibung | Standard |
|----------|--------------|----------|
| `LIVEKIT_URL` | LiveKit Server | - |
| `LIVEKIT_API_KEY` | API Key | - |
| `LIVEKIT_API_SECRET` | API Secret | - |
| `PIPER_URL` | Piper TTS Server | http://localhost:5000/ |
| `OLLAMA_BASE_URL` | Ollama API | http://localhost:11434/v1 |
| `OLLAMA_MODEL` | LLM-Modell | llama3.1 |
| `WHISPER_MODEL` | STT-Modell | base |
| `WHISPER_LANGUAGE` | STT-Sprache | de |
| `WHISPER_DEVICE` | CPU/CUDA | auto |

---

## Ausführung

```bash
# Mit uv (Python 3.10+)
uv run agent.py download-files   # Modelle
uv run agent.py console          # Terminal
uv run agent.py dev              # LiveKit

# Mit run.sh
./run.sh console
./run.sh dev
```

---

## Nächste Schritte (Backlog)

- [ ] Piper deutsche Stimme (de_DE-thorsten-medium) dokumentiert
- [ ] Termin-Tools mit echtem Backend verbinden
- [ ] Tests für Agent und Tools
- [ ] Docker-Setup für einfaches Deployment
