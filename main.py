import queue
import threading
from speech_loop import speech_loop
from shaking_detection import shaking_detect_loop
from image_analysis import ImageAnalyst
from dc import run_discord_bot


q = queue.Queue()
threading.Thread(target=speech_loop, args=(q,), daemon=True).start()
threading.Thread(target=shaking_detect_loop, args=(q,), daemon=True).start()
run_discord_bot(q)
