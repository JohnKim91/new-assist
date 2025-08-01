from pathlib import Path
import time

try:
    from pygame import mixer
except ImportError:  # pragma: no cover - optional dependency
    mixer = None


def init() -> None:
    """Initialize the mixer if available."""
    if mixer and not mixer.get_init():
        mixer.init()


def quit() -> None:
    """Quit the mixer if it was initialized."""
    if mixer and mixer.get_init():
        mixer.quit()


def play_audio(file_path: Path) -> None:
    """Play an audio file using pygame if available."""
    if not mixer:
        print(f"Would play audio: {file_path}")
        return
    mixer.music.load(str(file_path))
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)
