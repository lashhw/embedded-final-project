import speech_recognition as sr


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