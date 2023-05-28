import queue
import threading
from speech_loop import speech_loop
from shaking_detect import shaking_detect_loop
from dc import run_discord_bot


class AssistanceSystem:
    def __init__(self):
        self.q = queue.Queue()
        self.speech_thread = threading.Thread(
            target=speech_loop, args=(self.q,), daemon=True
        )
        self.shaking_detect_thread = threading.Thread(
            target=shaking_detect_loop, args=(self.q,), daemon=True
        )

    def run(self):
        self.speech_thread.start()
        self.shaking_detect_thread.start()
        run_discord_bot(self.q)


if __name__ == "__main__":
    assistance_system = AssistanceSystem()
    assistance_system.run()
