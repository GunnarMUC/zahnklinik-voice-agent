# Push-Anleitung: Zahnklinik Voice Agent zu GitHub

Das Projekt liegt bereit unter **`/Users/ai_dev/zahnklinik-voice-agent`**.

## Schritt 1: Repository auf GitHub anlegen

1. Öffne [github.com/new](https://github.com/new)
2. **Repository name:** `zahnklinik-voice-agent`
3. **Description:** Lokaler Echtzeit-Sprach-Assistent für Zahnkliniken
4. **Public** auswählen
5. **NICHT** "Add a README" oder andere Dateien hinzufügen (Repo leer lassen)
6. Auf **Create repository** klicken

## Schritt 2: Push ausführen

```bash
cd /Users/ai_dev/zahnklinik-voice-agent
git push -u origin main
```

Falls du noch nicht eingeloggt bist, wird Git nach deinen Zugangsdaten fragen.

## Inhalt des Repos

- `agent.py` – Haupt-Agent
- `whisper_stt.py` – Faster-Whisper STT
- `config.py` – Konfiguration
- `PROJEKT.md` – Ausführliche Projektbeschreibung
- `README.md` – Kurzanleitung
- `plan.md` – Projektplan
- `requirements.txt`, `pyproject.toml`, `run.sh`, `.env.example`
