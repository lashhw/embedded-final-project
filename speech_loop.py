import pvporcupine
from pvrecorder import PvRecorder
import tempfile
from image_analysis import image_analysis
from stt import stt
from tts import tts


def speech_loop(q, camera):
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
            elif "描述照片" in str:
                result = image_analysis(camera)
                tts(result["caption"], lang="en")
            elif "物件偵測" in str:
                result = image_analysis(camera)
                if len(result["objects"]) == 0:
                    text = "No object is detected."
                else:
                    text = f'I see {", ".join(result["objects"])}. '
                    if result["people_count"] != 0:
                        text += f'Totally {result["people_count"]} people are detected.'
                tts(text, lang="en")
            elif "圖片轉文字" in str:
                result = image_analysis(camera)
                tts(result["text"])
            else:
                tts("未知指令")
            recorder.start()
