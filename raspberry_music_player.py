# ================================================
# FILE: raspberry_music_player.py
# ================================================
"""Main orchestrator for PIR and NFC based music playback."""

from __future__ import annotations

import time

from pi_audio import (
    init_audio,
    cleanup_audio,
    play_random_intro,
    play_card_intro,
    play_card_audio,
)
from pi_sensors import (
    setup_gpio,
    cleanup_gpio,
    init_nfc_reader,
    read_nfc_uid,
    wait_for_button,
    is_pir_triggered,
)

COOLDOWN_SECONDS = 30 * 60  # 30 minutes


def main() -> None:
    setup_gpio()
    init_audio()
    pn532 = init_nfc_reader()
    last_trigger = 0

    try:
        while True:
            if is_pir_triggered():
                now = time.monotonic()
                if now - last_trigger > COOLDOWN_SECONDS:
                    last_trigger = now
                    play_random_intro()

            uid = read_nfc_uid(pn532)
            if uid:
                play_card_intro(uid)
                for _ in range(10):
                    print("Press the button to play the song…")
                    if wait_for_button(10):
                        play_card_audio(uid)
                        break

            time.sleep(0.1)
    finally:
        cleanup_gpio()
        cleanup_audio()


if __name__ == "__main__":
    main()
