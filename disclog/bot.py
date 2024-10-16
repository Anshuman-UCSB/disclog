import discord
from dotenv import load_dotenv
import os
import asyncio
import threading
import time

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variable
token = os.getenv("BOT_TOKEN")
BOT_CHANNEL = 551952998956269579

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

queue = asyncio.Queue()
queue.put_nowait("Hello, world!")
queue.put_nowait("Another message")


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    # Start the task to process the queue
    client.loop.create_task(process_queue())


async def process_queue():
    while True:
        message = await queue.get()
        channel = client.get_channel(BOT_CHANNEL)
        await channel.send(message)


def start_client():
    asyncio.run(client.start(token))


# Start the Discord client in a separate thread
thread = threading.Thread(target=start_client)
thread.start()

# Other code can run here
print("Discord client is running in a separate thread.")
for i in range(10):
    time.sleep(1)
    print("i =", i)
    queue.put_nowait(f"Message {i}")
