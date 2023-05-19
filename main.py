import discord
from discord import app_commands
from discord.ext import tasks
import queue
import sys
import select
import threading
from gtts import gTTS
import os
import tempfile
import pvporcupine
from pvrecorder import PvRecorder
import speech_recognition as sr


GUILD = discord.Object(id=1094156105606778940)
CONVERSATION_CHANNEL = 1094156105606778943
EMERGENCY_CHANNEL = 1094171915519791144

q = queue.Queue()


def tts(text, block=True):
    #print(f'output: {text}')
    filename = tempfile.mktemp()
    gTTS(text, lang='zh-TW').save(filename)
    command = f'ffplay -autoexit {filename} > /dev/null 2>&1 && rm {filename}'
    if not block:
        command += ' &'
    os.system(command)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
        self.proc_loop.start()

    @tasks.loop(seconds=1)
    async def proc_loop(self):
        while not q.empty():
            front = q.get_nowait()
            if front[0] == 'send_from':
                tts(front[1], False)
                await front[2].edit(content=f'已傳送「{front[1]}」')
            elif front[0] == 'send_to':
                await self.conv_channel.send(front[1])
                tts('已傳送訊息', False)
            elif front[0] == 'get_location':
                await front[1].edit(content='當前位置為')
    
    @proc_loop.before_loop
    async def before_proc_loop(self):
        await self.wait_until_ready()
        self.conv_channel = self.get_channel(CONVERSATION_CHANNEL)
        self.emer_channel = self.get_channel(EMERGENCY_CHANNEL)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
@app_commands.describe(text='要傳送的訊息')
async def send(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f'傳送「{text}」中...')
    msg = await interaction.original_response()
    q.put(['send_from', text, msg])


@client.tree.command()
async def get_location(interaction: discord.Interaction):
    await interaction.response.send_message('請稍等...')
    msg = await interaction.original_response()
    q.put(['get_location', msg])


def stt():
    '''
    i, _, _ = select.select([sys.stdin], [], [], timeout=10)
    if i:
        return sys.stdin.readline().strip()
    else:
        return None
    '''
    r = sr.Recognizer()
    text = None
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='zh-TW')
            print(f'Google Speech Recognition thinks you said {text}')
        except sr.UnknownValueError:
            print('Google Speech Recognition could not understand audio')
        except sr.RequestError as e:
            print(f'Could not request results from Google Speech Recognition service; {e}')
    return text

porcupine = pvporcupine.create(
  access_key='O+W0Bvushxv3+glLzhqPbSxmh5yYVbmxqCKG8gcFNxtyMdI+N+bOjQ==',
  keyword_paths=['keyword/pi.ppn'],
  model_path='keyword/porcupine_params_zh.pv'
)

recorder = PvRecorder(
    device_index=-1,
    frame_length=porcupine.frame_length
)
recorder.start()


def recv_loop():
    while True:
        pcm = recorder.read()
        result = porcupine.process(pcm)

        if result >= 0:
            recorder.stop()
            tts('請說指令')
            str = stt()
            if str is None:
                tts('未接收到指令')
            elif '傳送訊息' in str:
                tts('請說訊息')
                str = stt()
                if str is not None:
                    q.put_nowait(['send_to', str])
                else:
                    tts('未接收到訊息')
            else:
                tts('未知指令')
            recorder.start()


threading.Thread(target=recv_loop, daemon=True).start()
client.run('MTA5NDEwMjUwNjQ0NDk0NzQ3Ng.GlTrjK.sZlNWR-yfgWmWUZKbqA0iaidKrWN7gt0eFbOzI')
