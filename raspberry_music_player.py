from time import sleep
import RPi.GPIO as GPIO

from music_player.pir_handler import handle_pir
from music_player.nfc_handler import (
    open_clf,
    read_nfc_uid,
    play_card_intro,
    play_card_audio,
    prompt_button_press,
)
from music_player import audio_utils


def main() -> None:
    audio_utils.init()
    clf = open_clf()

    try:
        while True:
            handle_pir()
            uid = read_nfc_uid(clf)
            if uid:
                play_card_intro(uid)
                if prompt_button_press():
                    play_card_audio(uid)
            sleep(0.1)
    finally:
        if clf:
            clf.close()
        GPIO.cleanup()
        audio_utils.quit()


if __name__ == "__main__":
    main()
