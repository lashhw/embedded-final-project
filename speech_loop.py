import pvporcupine
from pvrecorder import PvRecorder
from stt import stt
from tts import tts


def speech_loop(q):
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
                else:
                    tts("未接收到訊息")
            else:
                tts("未知指令")
            recorder.start()