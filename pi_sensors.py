# ================================================
# FILE: pi_sensors.py
# ================================================
"""GPIO and NFC helper functions for the Raspberry Pi music player."""

from __future__ import annotations

import time

try:
    import RPi.GPIO as GPIO
except RuntimeError as exc:  # pragma: no cover - requires hardware
    raise RuntimeError(
        "This script must be run on a Raspberry Pi with RPi.GPIO installed"
    ) from exc

try:
    from pn532 import PN532_I2C
except ImportError:  # pragma: no cover - optional dependency
    PN532_I2C = None  # type: ignore

PIR_PIN = 17
BUTTON_PIN = 27


def setup_gpio() -> None:
    """Configure GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def cleanup_gpio() -> None:
    """Reset GPIO configuration."""
    GPIO.cleanup()


def init_nfc_reader():
    """Initialize the PN532 reader if available."""
    if PN532_I2C:
        pn532 = PN532_I2C(debug=False)
        pn532.SAM_configuration()
        return pn532
    return None


def wait_for_button(timeout: float) -> bool:
    """Return True if the button is pressed within timeout seconds."""
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.05)
            return True
        time.sleep(0.05)
    return False


def read_nfc_uid(pn532) -> str | None:
    """Read an NFC UID if present."""
    if not pn532:
        return None
    uid = pn532.read_passive_target(timeout=0.5)
    if uid:
        return "".join(f"{x:02X}" for x in uid)
    return None


def is_pir_triggered() -> bool:
    """Return True if the PIR sensor is active."""
    return GPIO.input(PIR_PIN) == GPIO.HIGH
