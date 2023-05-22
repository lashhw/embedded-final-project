import os
import tempfile
from gtts import gTTS


def tts(text, lang="zh-TW"):
    print(f'speaking "{text}"')
    filename = tempfile.mktemp()
    gTTS(text, lang=lang).save(filename)
    command = f"ffplay -autoexit {filename} > /dev/null 2>&1 && rm {filename}"
    os.system(command)
