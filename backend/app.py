from quart import Quart, request, jsonify
from asyncio import Queue

app = Quart(__name__)
message_queue = Queue()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/post_message", methods=["POST"])
async def post_message():
    data = await request.get_json()
    message = data.get("message")
    token = data.get("token")

    if not message or not token:
        return jsonify({"error": "Message and token are required"}), 400

    # await send_message(BOT_CHANNEL, "Received message: " + message)
    message_queue.put_nowait(message)

    # Process the message and token here
    # For example, you can print them or perform some action
    print(f"Received message: {message}")
    print(f"Received token: {token}")

    return jsonify({"status": "success", "message": message, "token": token}), 200
