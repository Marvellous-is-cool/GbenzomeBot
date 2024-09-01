from flask import Flask
from threading import Thread
from highrise.__main__ import *
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the values from the .env file
port = int(os.getenv('PORT', 8080))  # Default to 8080 if not set
room_id = os.getenv('ROOM_ID')
bot_token = os.getenv('BOT_TOKEN')

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return "Alive"

def run_flask():
    app.run(host='0.0.0.0', port=port)

class RunBot():
    def __init__(self) -> None:
        self.room_id = room_id
        self.bot_token = bot_token
        self.bot_file = "main"
        self.bot_class = "Bot"
        self.definitions = [
            BotDefinition(
                getattr(import_module(self.bot_file), self.bot_class)(),
                self.room_id, self.bot_token)
        ]

    def run_loop(self) -> None:
        while True:
            try:
                arun(main(self.definitions))
            except Exception as e:
                print("Error: ", e)
                time.sleep(5)

if __name__ == "__main__":
    # Start Flask app in a separate thread
    thread = Thread(target=run_flask)
    thread.start()

    # Run bot loop
    RunBot().run_loop()
