# Zahnklinik Voice Agent – Projektbeschreibung

**Stand:** 18. Februar 2025  
**Repository:** [github.com/GunnarMUC/zahnklinik-voice-agent](https://github.com/GunnarMUC/zahnklinik-voice-agent)

---

## 1. Projektziel

Entwicklung eines **lokalen Echtzeit-Sprach-Assistenten** für Zahnkliniken. Der Assistent soll:

- Patienten auf Deutsch ansprechen
- Sich den Namen des Patienten merken (Chat-Kontext)
- Bei Terminanfragen unterstützen (Platzhalter für spätere Integration)
- Vollständig lokal laufen (STT, LLM, TTS) – keine Cloud-Abhängigkeit für die Sprachverarbeitung

---

## 2. Technischer Stack

| Komponente | Technologie | Begründung |
|------------|-------------|------------|
| **Framework** | LiveKit Agents SDK (Python) | Echtzeit-Voice-Pipeline, Room-Management, Turn Detection |
| **STT** | Faster-Whisper | Lokal, Deutsch, gute Qualität |
| **LLM** | Ollama (llama3.1) | Lokal, keine API-Kosten |
| **TTS** | Piper | Lokal, deutsche Stimmen (z.B. de_DE-thorsten) |
| **VAD** | Silero | Lokale Spracherkennung für Turn Detection |

---

## 3. Architektur

```
Mikrofon → [Faster-Whisper STT] → [Ollama LLM] → [Piper TTS] → Lautsprecher
                    ↑                    ↑
              Silero VAD           Termin-Tools
              StreamAdapter        store_patient_name
```

- **StreamAdapter:** Whisper ist nicht streaming-fähig; VAD puffert Audio bis Ende der Äußerung.
- **Chat-Kontext:** `store_patient_name` speichert den Namen in `session.userdata`.
- **Tools:** Platzhalter für `check_appointment_availability`, `book_appointment`, `cancel_appointment`.

---

## 4. Projektstruktur

```
zahnklinik-voice-agent/
├── agent.py           # ZahnklinikAgent, AgentSession, Tools
├── whisper_stt.py     # Faster-Whisper STT-Adapter für LiveKit
├── config.py          # Konfiguration über Umgebungsvariablen
├── requirements.txt   # Python-Abhängigkeiten
├── pyproject.toml     # Projekt-Metadaten
├── run.sh             # Start-Skript (console/dev/start)
├── README.md          # Kurzanleitung
├── plan.md            # Projektplan und Status
├── PROJEKT.md         # Diese ausführliche Beschreibung
├── .env.example       # Vorlage für Umgebungsvariablen
└── .env.local         # Credentials (nicht im Repo)
```

---

## 5. Implementierungsdetails

### 5.1 agent.py

- **ZahnklinikAgent:** Erbt von `Agent`, deutsche System-Instructions, vier Tools.
- **Tools:**
  - `store_patient_name(name)` – speichert Patientennamen
  - `check_appointment_availability(date?)` – Platzhalter
  - `book_appointment(datetime_slot, patient_name?)` – Platzhalter
  - `cancel_appointment(appointment_id)` – Platzhalter
- **AgentSession:** STT (StreamAdapter + Whisper), LLM (Ollama), TTS (Piper), VAD, Multilingual Turn Detector.

### 5.2 whisper_stt.py

- Basiert auf [livekit-whisper](https://github.com/taresh18/livekit-whisper).
- Implementiert `_recognize_impl` für LiveKit STT-Interface.
- Konfigurierbar: Modell (base/small/medium), Sprache (de), Device (auto/cpu/cuda).

### 5.3 config.py

- Lädt `.env.local`.
- Zentrale Werte: `LIVEKIT_*`, `OLLAMA_*`, `PIPER_URL`, `WHISPER_*`.

---

## 6. Voraussetzungen

- **Python 3.10+** (LiveKit Agents)
- **Ollama** mit `ollama run llama3.1`
- **Piper TTS Server** (z.B. `python3 -m piper.http_server -m de_DE-thorsten-medium`)
- **LiveKit** Account für dev/start (Console-Modus ohne LiveKit möglich)

---

## 7. Installation und Start

```bash
# Abhängigkeiten
uv venv --python 3.12
uv pip install -r requirements.txt

# Konfiguration
cp .env.example .env.local
# LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET eintragen

# Modelle
uv run agent.py download-files

# Ausführung
uv run agent.py console   # Terminal
uv run agent.py dev       # LiveKit
```

---

## 8. Nächste Schritte (Backlog)

- [ ] Termin-Tools mit echtem Kalender/Backend verbinden
- [ ] Piper deutsche Stimme in Doku hervorheben
- [ ] Unit-Tests für Agent und Tools
- [ ] Docker-Setup für Deployment
- [ ] Optional: Noise Cancellation für Telefonie

---

## 9. Lizenz und Kontakt

Projekt für [GunnarMUC](https://github.com/GunnarMUC) – Zahnklinik Voice Agent.
