import queue
import threading
from speech_loop import speech_loop
from shaking_detection import ShakingDetector
from dc import run_discord_bot


def shaking_detect_loop():
    sd = ShakingDetector()
    while True:
        sd.detect(q)


q = queue.Queue()
threading.Thread(target=speech_loop, args=(q,), daemon=True).start()
threading.Thread(target=shaking_detect_loop, daemon=True).start()
run_discord_bot(q)