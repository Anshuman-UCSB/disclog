import discord
from dotenv import load_dotenv
import os
from backend.app import app, message_queue
from backend.sql import register_user, get_cid

load_dotenv()
token = os.getenv("BOT_TOKEN")


def exception_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred in {func.__name__}: {e}")

    return wrapper


class Discbot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @exception_handler
    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.logging_handler())
        self.webapi = self.loop.create_task(app.run_task())

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    @exception_handler
    async def logging_handler(self):
        await self.wait_until_ready()
        print("Logging handler ready")
        while not self.is_closed():
            message, username, token = await message_queue.get()
            print("Processing {}, {}, {}".format(message, username, token))
            cid = get_cid(username, token)
            if cid:
                print("Got channel id", cid)
                channel = self.get_channel(cid) or await self.fetch_channel(cid)
                print("channel:", channel)
                if channel:
                    await channel.send(message)
                    print("Message sent to channel {}".format(channel))
            else:
                print("Invalid username/token combo")

    @exception_handler
    async def on_message(self, message):
        if (
            isinstance(message.channel, discord.DMChannel)
            and message.author != self.user
        ):
            print(
                f"Message received in channel: {message.channel} (ID: {message.channel.id})"
                f" - {message.author} - {message.author.id}"
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
