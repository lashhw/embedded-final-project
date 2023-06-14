import os
import discord
from discord import app_commands
from discord.ext import tasks
from location_utils import get_current_address
from speech_loop import tts


GUILD = discord.Object(id=1094156105606778940)
CONVERSATION_CHANNEL = 1094156105606778943
EMERGENCY_CHANNEL = 1094171915519791144


class MyClient(discord.Client):
    def __init__(self, q, intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.q = q

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
        self.proc_loop.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    @tasks.loop(seconds=1)
    async def proc_loop(self):
        while not self.q.empty():
            front = self.q.get_nowait()
            if front[0] == "send_from":
                tts("收到訊息")
                tts(front[1])
                await front[2].edit(content=f"已傳送「{front[1]}」")
            elif front[0] == "send_to":
                await self.conv_channel.send(front[1])
            elif front[0] == "send_picture":
                await self.conv_channel.send(file=discord.File(front[1]))
                os.system(f"rm -f {front[1]}")
            elif front[0] == "get_location":
                address = await get_current_address()
                await front[1].edit(content=f"當前位置為 {address}")
            elif front[0] == "shaking":
                await self.emer_channel.send("出事了阿伯")
            else:
                print("未知指令")

    @proc_loop.before_loop
    async def before_proc_loop(self):
        await self.wait_until_ready()
        self.conv_channel = self.get_channel(CONVERSATION_CHANNEL)
        self.emer_channel = self.get_channel(EMERGENCY_CHANNEL)


def run_discord_bot(q):
    client = MyClient(q, discord.Intents.default())

    @client.tree.command()
    @app_commands.describe(text="要傳送的訊息")
    async def send(interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f"傳送「{text}」中...")
        msg = await interaction.original_response()
        q.put(["send_from", text, msg])

    @client.tree.command()
    async def get_location(interaction: discord.Interaction):
        await interaction.response.send_message("請稍等...")
        msg = await interaction.original_response()
        q.put(["get_location", msg])

    client.run(
        "MTA5NDEwMjUwNjQ0NDk0NzQ3Ng.GlTrjK.sZlNWR-yfgWmWUZKbqA0iaidKrWN7gt0eFbOzI"
    )
