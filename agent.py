"""
Lokaler Echtzeit-Sprach-Assistent für Zahnklinik.
LiveKit Agents SDK mit Faster-Whisper (STT), Ollama (LLM), Piper (TTS).
"""

import logging
import urllib.request
from typing import Any

import config
from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, function_tool, room_io
from livekit.agents.voice import RunContext
from livekit.plugins import openai, piper_tts, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from whisper_stt import WhisperSTT
from livekit.agents.stt import StreamAdapter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("zahnklinik-agent")

# System-Instructions für den Zahnklinik-Assistenten (Deutsch)
BASE_INSTRUCTIONS = """Du bist ein freundlicher Sprach-Assistent einer Zahnklinik.
Du sprichst ausschließlich Deutsch.
Deine Antworten sind kurz, prägnant und ohne Emojis oder Sonderzeichen.
Du hilfst Patienten bei Terminanfragen, allgemeinen Fragen zur Praxis und leitest bei Bedarf weiter.

Wenn sich ein Patient mit seinem Namen vorstellt, rufe die Funktion store_patient_name auf, um den Namen zu speichern.
Verwende den gespeicherten Namen in der weiteren Ansprache.

Für Terminanfragen nutze die verfügbaren Tools. 
Beachte: Die Terminbuchung ist derzeit eine Demo ohne Anbindung an ein echtes Praxis-System.
Bei Buchungsanfragen weise den Patienten stets darauf hin, dass das Praxisteam sich zur Bestätigung melden wird."""


class ZahnklinikAgent(Agent):
    """Voice Agent für die Zahnklinik mit Chat-Kontext und Termin-Tools."""

    def __init__(self, patient_name: str | None = None) -> None:
        instructions = BASE_INSTRUCTIONS
        if patient_name:
            instructions += f"\n\nDer Patient heißt {patient_name}. Verwende diesen Namen in der Ansprache."

        super().__init__(
            instructions=instructions,
            tools=[
                self.store_patient_name,
                self.check_appointment_availability,
                self.book_appointment,
                self.cancel_appointment,
            ],
        )

    @function_tool()
    async def store_patient_name(
        self,
        context: RunContext,
        name: str,
    ) -> str:
        """Speichert den Namen des Patienten für die weitere Konversation.
        Rufe diese Funktion auf, wenn der Patient sich mit seinem Namen vorstellt.

        Args:
            name: Der vollständige Name des Patienten.
        """
        if hasattr(context, "userdata") and context.userdata is not None:
            context.userdata["patient_name"] = name
            return f"Name {name} wurde gespeichert."
        return f"Name {name} zur Kenntnis genommen."

    @function_tool()
    async def check_appointment_availability(
        self,
        context: RunContext,
        date: str | None = None,
    ) -> dict[str, Any]:
        """Prüft die Verfügbarkeit von Terminen.
        Platzhalter für spätere Terminbuchungs-Integration.

        Args:
            date: Optionales Datum im Format JJJJ-MM-TT. Wenn nicht angegeben, wird das aktuelle Datum verwendet.
        """
        return {
            "available": True,
            "slots": ["2025-02-20 10:00", "2025-02-20 14:00", "2025-02-21 09:00"],
            "message": "Demo-Umgebung — Termin-Slots sind Beispiele ohne echte Verfügbarkeit.",
        }

    @function_tool()
    async def book_appointment(
        self,
        context: RunContext,
        datetime_slot: str,
        patient_name: str | None = None,
    ) -> dict[str, Any]:
        """Bucht einen Termin für den angegebenen Zeitpunkt.
        Platzhalter für spätere Terminbuchungs-Integration.

        Args:
            datetime_slot: Gewünschter Termin (z.B. "2025-02-20 10:00").
            patient_name: Optional - Name des Patienten, falls bekannt.
        """
        return {
            "success": False,
            "appointment_id": "demo-buchung",
            "datetime": datetime_slot,
            "message": "Demo-Buchung: Kein echter Termin gespeichert. Terminvergabe-System muss angebunden werden.",
        }

    @function_tool()
    async def cancel_appointment(
        self,
        context: RunContext,
        appointment_id: str,
    ) -> dict[str, Any]:
        """Storniert einen bestehenden Termin.
        Platzhalter für spätere Terminbuchungs-Integration.

        Args:
            appointment_id: Die ID des zu stornierenden Termins.
        """
        return {
            "success": False,
            "message": f"Demo-Stornierung: Kein echter Termin {appointment_id} storniert. Terminvergabe-System muss angebunden werden.",
        }


def create_session() -> AgentSession:
    """Erstellt eine AgentSession mit STT, LLM, TTS und VAD."""
    whisper_stt = WhisperSTT(
        language=config.WHISPER_LANGUAGE,
        model=config.WHISPER_MODEL,
        device=config.WHISPER_DEVICE,
        compute_type=config.WHISPER_COMPUTE_TYPE,
    )
    vad = silero.VAD.load()
    stt = StreamAdapter(stt=whisper_stt, vad=vad)

    llm = openai.LLM.with_ollama(
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL,
    )

    tts = piper_tts.TTS(config.PIPER_URL)

    return AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=vad,
        turn_detection=MultilingualModel(),
        userdata={"patient_name": None},
    )


def _verify_services() -> None:
    """Warn at startup if Ollama or Piper TTS are unreachable."""
    try:
        urllib.request.urlopen(f"{config.OLLAMA_BASE_URL}/models", timeout=3)
        logger.info("Ollama erreichbar unter %s", config.OLLAMA_BASE_URL)
    except Exception:
        logger.warning("Ollama nicht erreichbar unter %s", config.OLLAMA_BASE_URL)

    try:
        urllib.request.urlopen(config.PIPER_URL, timeout=3)
        logger.info("Piper TTS erreichbar unter %s", config.PIPER_URL)
    except Exception:
        logger.warning("Piper TTS nicht erreichbar unter %s", config.PIPER_URL)


server = AgentServer()


@server.rtc_session(agent_name="zahnklinik-agent")
async def zahnklinik_agent(ctx: agents.JobContext) -> None:
    """Entrypoint für den Zahnklinik Voice Agent."""
    logger.info("Zahnklinik Agent gestartet für Room %s", ctx.room.name)
    _verify_services()
    session = create_session()

    agent = ZahnklinikAgent(patient_name=None)

    await session.start(
        room=ctx.room,
        agent=agent,
        room_options=room_io.RoomOptions(),
    )

    await session.generate_reply(
        instructions="Begrüße den Patienten freundlich auf Deutsch und biete deine Hilfe an."
    )


def main() -> None:
    """CLI-Einstiegspunkt. Validiert Konfiguration und startet den Agent-Server."""
    config._validate_config()
    agents.cli.run_app(server)


if __name__ == "__main__":
    main()
