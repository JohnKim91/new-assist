# ================================================
# FILE: pi_audio.py
# ================================================
"""Audio helper functions for the Raspberry Pi music player."""

from __future__ import annotations

import random
import time
from pathlib import Path

try:
    from pygame import mixer
except ImportError:  # pragma: no cover - optional dependency
    mixer = None  # type: ignore

INTRO_AUDIO_DIR = Path("pir_prompts")
CARD_INTRO_DIR = Path("card_intros")
CARD_AUDIO_DIR = Path("card_audio")

# Mapping of NFC card UID (hex string) to audio file name in CARD_AUDIO_DIR
CARD_AUDIO_MAP: dict[str, str] = {
    # Example: "04A1B2C3D4": "song1.mp3",
}


def init_audio() -> None:
    """Initialize pygame mixer if available."""
    if mixer:
        mixer.init()


def cleanup_audio() -> None:
    """Cleanup pygame mixer."""
    if mixer:
        mixer.quit()


def play_audio(file_path: Path) -> None:
    """Play an audio file or log if mixer is unavailable."""
    if not mixer:
        print(f"Would play audio: {file_path}")
        return
    mixer.music.load(str(file_path))
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)


def play_random_intro() -> None:
    """Play a random introduction audio clip."""
    files = list(INTRO_AUDIO_DIR.glob("*.mp3"))
    if not files:
        return
    play_audio(random.choice(files))


def play_card_intro(card_uid: str) -> None:
    """Play card introduction audio if present."""
    path = CARD_INTRO_DIR / f"{card_uid}.mp3"
    if path.exists():
        play_audio(path)


def play_card_audio(card_uid: str) -> None:
    """Play the audio mapped to a specific card UID."""
    filename = CARD_AUDIO_MAP.get(card_uid)
    if filename:
        path = CARD_AUDIO_DIR / filename
        if path.exists():
            play_audio(path)
