import logging
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv("API_URL")


class DisclogHandler(logging.Handler):
    def __init__(self, username, token, *args, **kwargs):
        self.username = username
        self.token = token
        super().__init__(*args, **kwargs)

    def emit(self, record):
        # This method is called every time a log message is emitted
        log_message = self.format(record)

        # Here you can redirect the message to your custom handler
        self.send_to_disclog(log_message)

    def send_to_disclog(self, message):
        # Your custom logic for handling the message goes here
        # For example, store it, send it to a server, etc.
        print(f"Disclog received message: {message}")

        # send a POST request to the endpoint /post_message with the data message, username, and token
        # For example, using requests library:
        print("posting to", API_URL)
        response = requests.post(
            API_URL,
            json={"message": message, "username": self.username, "token": self.token},
        )
        print("Got response", response.text)


def create_logger(
    username, token, level=logging.INFO, *args, **kwargs
) -> logging.Logger:
    # Create your logger
    logger = logging.getLogger("disclog")
    logger.setLevel(level)

    # Add the custom handler
    handler = DisclogHandler(username=username, token=token, *args, **kwargs)
    # formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


if __name__ == "__main__":
    USERNAME = os.getenv("USERNAME")
    TOKEN = os.getenv("TOKEN")
    # Create the logger
    logger = create_logger(
        username=USERNAME,
        token=TOKEN,
        level=logging.DEBUG,
    )
    logger.debug("This is a debug message")
    logger.info("This is a info message")
