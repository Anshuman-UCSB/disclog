import discord
from dotenv import load_dotenv
import os
from backend.app import app, message_queue
from backend.sql import register_user

load_dotenv()

token = os.getenv("BOT_TOKEN")
BOT_CHANNEL = 551952998956269579


class Discbot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    async def on_message(self, message):
        if (
            isinstance(message.channel, discord.DMChannel)
            and message.author != self.user
        ):
            print(
                f"Message received in channel: {message.channel} (ID: {message.channel.id}) - {message.author} - {message.author.id}"
            )
            token = register_user(
                message.author.id, str(message.author), message.channel.id
            )
            # respond with the token
            await message.author.send(f"Your token is: ||{token}||")


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    client = Discbot(intents=intents)
    client.run(token)
