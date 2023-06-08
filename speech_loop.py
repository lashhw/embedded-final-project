import os
import pvporcupine
import speech_recognition as sr
import tempfile
from pvrecorder import PvRecorder
from gtts import gTTS
from image_analysis import ImageAnalyst
from location_utils import get_current_address
import os


def stt():
    r = sr.Recognizer()
    text = None
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="zh-TW")
            print(f'you said "{text}"')
        except sr.UnknownValueError:
            print("could not understand")
        except sr.RequestError as e:
            print(e)
    return text


def tts(text, lang="zh-TW"):
    print(f'speaking "{text}"')
    filename = tempfile.mktemp()
    gTTS(text, lang=lang).save(filename)
    command = f"ffplay -autoexit {filename} > /dev/null 2>&1 && rm {filename}"
    os.system(command)


def speech_loop(q, camera):
    image_analyst = ImageAnalyst()

    porcupine = pvporcupine.create(
        access_key="O+W0Bvushxv3+glLzhqPbSxmh5yYVbmxqCKG8gcFNxtyMdI+N+bOjQ==",
        keyword_paths=["keyword/pi.ppn"],
        model_path="keyword/porcupine_params_zh.pv",
    )

    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    recorder.start()

    while True:
        pcm = recorder.read()
        result = porcupine.process(pcm)

        if result >= 0:
            recorder.stop()

            tts("請說指令")

            str = stt()
            if str is None:
                tts("未接收到指令")
            elif "傳送訊息" in str:
                tts("請說訊息")
                str = stt()
                if str is not None:
                    q.put_nowait(["send_to", str])
                    tts("已傳送訊息")
                else:
                    tts("未接收到訊息")
            elif "傳送照片" in str:
                filename = f"{tempfile.mktemp()}.png"
                camera.capture(filename)
                q.put_nowait(["send_picture", filename])
                tts("已傳送照片")
            elif "當前位置" in str or "我在哪" in str:
                address = get_current_address()
                tts(f"當前位置為 {address}")
            elif "描述照片" in str:
                result = image_analyst.analysis()
                tts(result["caption"], lang="en")
            elif "物件偵測" in str:
                result = image_analyst.analysis()
                if len(result["objects"]) == 0:
                    text = "No object is detected."
                else:
                    text = f'I see {", ".join(result["objects"])}. '
                    if result["people_count"] != 0:
                        text += f'Totally {result["people_count"]} people are detected.'
                tts(text, lang="en")
            elif "圖片轉文字" in str:
                result = image_analyst.analysis()
                tts(result["text"])
            elif "google" in str.lower():
                tts("請說")
                os.system("googlesamples-assistant-pushtotalk --once")
            else:
                tts("未知指令")

            recorder.start()
