import discord
from dotenv import load_dotenv
import os
import asyncio
from backend.app import app, message_queue

load_dotenv()

token = os.getenv("BOT_TOKEN")
BOT_CHANNEL = 551952998956269579


class Discbot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = asyncio.Queue()
        self.queue.put_nowait("Hello, world!")
        self.queue.put_nowait("Another message")

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())
        self.webapi = self.loop.create_task(app.run_task())

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(BOT_CHANNEL)  # channel ID goes here
        while not self.is_closed():
            message = await message_queue.get()
            await channel.send(message)


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    client = Discbot(intents=intents)
    client.run(token)
