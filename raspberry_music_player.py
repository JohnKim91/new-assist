from time import sleep
import RPi.GPIO as GPIO

from music_player.pir_handler import handle_pir
from music_player.nfc_handler import (
    PN532_I2C,
    read_nfc_uid,
    play_card_intro,
    play_card_audio,
    wait_for_button,
)
from music_player import audio_utils


def main() -> None:
    audio_utils.init()
    pn532 = None
    if PN532_I2C:
        pn532 = PN532_I2C(debug=False)
        pn532.SAM_configuration()

    try:
        while True:
            handle_pir()
            uid = read_nfc_uid(pn532)
            if uid:
                play_card_intro(uid)
                for _ in range(10):
                    print("Press the button to play the song…")
                    if wait_for_button(10):
                        play_card_audio(uid)
                        break
            sleep(0.1)
    finally:
        GPIO.cleanup()
        audio_utils.quit()


if __name__ == "__main__":
    main()
