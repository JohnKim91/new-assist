from pathlib import Path
import random
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:  # pragma: no cover - requires hardware
    raise RuntimeError("This script must be run on a Raspberry Pi with RPi.GPIO installed")

from .audio_utils import play_audio

PIR_PIN = 17
COOLDOWN_SECONDS = 30 * 60  # 30 minutes
INTRO_AUDIO_DIR = Path("pir_prompts")

last_trigger = 0.0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)


def play_random_intro() -> None:
    files = list(INTRO_AUDIO_DIR.glob("*.mp3"))
    if files:
        play_audio(random.choice(files))


def handle_pir() -> None:
    """Check PIR sensor and play intro if cooldown elapsed."""
    global last_trigger
    if GPIO.input(PIR_PIN):
        now = time.monotonic()
        if now - last_trigger > COOLDOWN_SECONDS:
            last_trigger = now
            play_random_intro()
