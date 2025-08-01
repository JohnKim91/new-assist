from pathlib import Path
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:  # pragma: no cover - requires hardware
    raise RuntimeError("This script must be run on a Raspberry Pi with RPi.GPIO installed")

try:
    from pn532 import PN532_I2C
except ImportError:  # pragma: no cover - optional dependency
    PN532_I2C = None  # type: ignore

from .audio_utils import play_audio

BUTTON_PIN = 27
CARD_INTRO_DIR = Path("card_intros")
CARD_AUDIO_DIR = Path("card_audio")
CARD_AUDIO_MAP: dict[str, str] = {}

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def read_nfc_uid(pn532) -> str | None:
    if not pn532:
        return None
    uid = pn532.read_passive_target(timeout=0.5)
    if uid:
        return "".join(f"{x:02X}" for x in uid)
    return None


def wait_for_button(timeout: float) -> bool:
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.05)
            return True
        time.sleep(0.05)
    return False


def play_card_intro(card_uid: str) -> None:
    path = CARD_INTRO_DIR / f"{card_uid}.mp3"
    if path.exists():
        play_audio(path)


def play_card_audio(card_uid: str) -> None:
    filename = CARD_AUDIO_MAP.get(card_uid)
    if filename:
        path = CARD_AUDIO_DIR / filename
        if path.exists():
            play_audio(path)
