"""
Faster-Whisper STT plugin for LiveKit Agents.
Based on https://github.com/taresh18/livekit-whisper
"""

import dataclasses
import logging
import os
import time
from dataclasses import dataclass
from typing import Optional

import numpy as np
from faster_whisper import WhisperModel

from livekit import rtc
from livekit.agents import APIConnectionError, APIConnectOptions, stt
from livekit.agents.utils import AudioBuffer

logger = logging.getLogger(__name__)


@dataclass
class WhisperOptions:
    """Configuration options for WhisperSTT."""

    language: str
    model: str
    device: Optional[str]
    compute_type: Optional[str]
    model_cache_directory: Optional[str]
    warmup_audio: Optional[str]


class WhisperSTT(stt.STT):
    """STT implementation using Faster-Whisper model."""

    def __init__(
        self,
        model: str = "base",
        language: str = "de",
        device: Optional[str] = None,
        compute_type: Optional[str] = None,
        model_cache_directory: Optional[str] = None,
        warmup_audio: Optional[str] = None,
    ):
        """Initialize the WhisperSTT instance.

        Args:
            model: Whisper model to use (base, small, medium, large-v3, etc.)
            language: Language code for speech recognition (de for German)
            device: Device to use for inference (cuda, cpu, auto)
            compute_type: Compute type for inference (float16, int8, float32)
            model_cache_directory: Directory to store downloaded models
            warmup_audio: Path to audio file for model warmup
        """
        super().__init__(
            capabilities=stt.STTCapabilities(streaming=False, interim_results=False)
        )

        self._opts = WhisperOptions(
            language=language,
            model=model,
            device=device or "auto",
            compute_type=compute_type or "float32",
            model_cache_directory=model_cache_directory,
            warmup_audio=warmup_audio,
        )

        self._model: Optional[WhisperModel] = None
        self._initialize_model()

        if warmup_audio and os.path.exists(warmup_audio):
            try:
                import soundfile as sf

                self._warmup(warmup_audio, sf)
            except ImportError:
                logger.warning("soundfile not installed, skipping warmup")

    def _initialize_model(self) -> None:
        """Initialize the Whisper model."""
        device = self._opts.device
        compute_type = self._opts.compute_type

        logger.info("Using device: %s, with compute: %s", device, compute_type)

        model_cache_dir = self._opts.model_cache_directory
        if model_cache_dir:
            os.makedirs(model_cache_dir, exist_ok=True)
            logger.info("Using model cache directory: %s", model_cache_dir)

        self._model = WhisperModel(
            model_size_or_path=str(self._opts.model),
            device=device or "auto",
            compute_type=compute_type or "float32",
            download_root=model_cache_dir,
        )
        logger.info("Whisper model loaded successfully")

    def _warmup(self, warmup_audio_path: str, sf) -> None:
        """Perform a warmup transcription."""
        logger.info("Starting STT engine warmup using %s...", warmup_audio_path)
        try:
            start_time = time.time()
            warmup_audio_data, _ = sf.read(warmup_audio_path, dtype="float32")
            segments, _ = self._model.transcribe(
                warmup_audio_data, language=self._opts.language, beam_size=1
            )
            model_warmup_transcription = " ".join(segment.text for segment in segments)
            warmup_time = time.time() - start_time
            logger.info(
                "STT engine warmed up in %.1fms. Text: %s",
                warmup_time * 1000,
                model_warmup_transcription,
            )
        except Exception as e:
            logger.error("Failed to warm up STT engine: %s", e)

    def _sanitize_options(self, *, language: Optional[str] = None) -> WhisperOptions:
        """Create a copy of options with optional overrides."""
        options = dataclasses.replace(self._opts)
        if language:
            options.language = language
        return options

    async def _recognize_impl(
        self,
        buffer: AudioBuffer,
        *,
        language: Optional[str],
        conn_options: APIConnectOptions,
    ) -> stt.SpeechEvent:
        """Implement speech recognition."""
        if self._model is None:
            raise APIConnectionError("Whisper model not initialized")

        try:
            logger.debug("Received audio, transcribing to text")
            options = self._sanitize_options(language=language)

            combined_frame = rtc.combine_audio_frames(buffer)
            raw_bytes = bytes(combined_frame.data)
            audio_array = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0

            start_time = time.time()
            segments, info = self._model.transcribe(
                audio_array,
                language=options.language or None,
                beam_size=1,
                best_of=1,
                condition_on_previous_text=True,
                vad_filter=False,
                vad_parameters=dict(min_silence_duration_ms=500),
            )

            segments_list = list(segments)
            full_text = " ".join(segment.text.strip() for segment in segments_list)
            inference_time = time.time() - start_time

            logger.info(
                "STT inference completed in %.1fms. Text: %s",
                inference_time * 1000,
                full_text,
            )

            return stt.SpeechEvent(
                type=stt.SpeechEventType.FINAL_TRANSCRIPT,
                alternatives=[
                    stt.SpeechData(
                        text=full_text or "",
                        language=options.language or "de",
                    )
                ],
            )

        except Exception as e:
            logger.error("Error in speech recognition: %s", e, exc_info=True)
            raise APIConnectionError() from e
