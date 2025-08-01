from time import sleep
import RPi.GPIO as GPIO

from music_player.pir_handler import handle_pir
from music_player.nfc_handler import (
    open_clf,
    read_nfc_uid,
    play_card_intro,
    play_card_audio,
    wait_for_button,
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
                for _ in range(10):
                    print("Press the button to play the song…")
                    if wait_for_button(10):
                        play_card_audio(uid)
                        break
            sleep(0.1)
    finally:
        if clf:
            clf.close()
        GPIO.cleanup()
        audio_utils.quit()


if __name__ == "__main__":
    main()
