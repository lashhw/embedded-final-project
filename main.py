import queue
import picamera
import threading
from speech_loop import speech_loop
from shaking_detection import shaking_detect_loop
from dc import run_discord_bot


q = queue.Queue()
camera = picamera.PiCamera()
threading.Thread(target=speech_loop, args=(q, camera), daemon=True).start()
threading.Thread(target=shaking_detect_loop, args=(q,), daemon=True).start()
run_discord_bot(q)