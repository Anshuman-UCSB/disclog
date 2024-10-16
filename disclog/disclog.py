import logging


class DisclogHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
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


def create_logger() -> logging.Logger:
    # Create your logger
    logger = logging.getLogger("disclog")
    logger.setLevel(logging.INFO)

    # Add the custom handler
    handler = DisclogHandler()
    # formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = create_logger()
