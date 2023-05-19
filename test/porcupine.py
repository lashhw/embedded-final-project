import pvporcupine
from pvrecorder import PvRecorder
from gtts import gTTS
import speech_recognition as sr
import os


def tts(text):
    gTTS(text, lang='zh-TW').save('/tmp/sound.mp3')
    os.system('ffplay -autoexit /tmp/sound.mp3')


porcupine = pvporcupine.create(
  access_key='O+W0Bvushxv3+glLzhqPbSxmh5yYVbmxqCKG8gcFNxtyMdI+N+bOjQ==',
  keyword_paths=['keyword/pi.ppn'],
  model_path='keyword/porcupine_params_zh.pv'
)

for i, device in enumerate(PvRecorder.get_audio_devices()):
    print(f'Device {i}: {device}')

recorder = PvRecorder(
    device_index=-1,
    frame_length=porcupine.frame_length
)
recorder.start()

print('Listening ... (press Ctrl+C to exit)')
try:
    while True:
        pcm = recorder.read()
        result = porcupine.process(pcm)

        if result >= 0:
            recorder.stop()
            tts('請說指令')
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
                try:
                    print('Google Speech Recognition thinks you said ' + r.recognize_google(audio, language='zh-TW'))
                except sr.UnknownValueError:
                    print('Google Speech Recognition could not understand audio')
                except sr.RequestError as e:
                    print(f'Could not request results from Google Speech Recognition service; {e}')
                except KeyboardInterrupt:
                    print('Stopping ...')
            recorder.start()
finally:
    recorder.delete()
    porcupine.delete()