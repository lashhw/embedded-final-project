import os
import tempfile
from gtts import gTTS


def tts(text, blocking=True):
    # print(f'output: {text}')
    filename = tempfile.mktemp()
    gTTS(text, lang="zh-TW").save(filename)
    command = f"ffplay -autoexit {filename} > /dev/null 2>&1 && rm {filename}"
    if not blocking:
        command += " &"
    os.system(command)
