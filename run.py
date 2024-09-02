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

# Flask web server setup
class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Alive"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=port)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()

# Bot setup and loop
class RunBot:
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

# Gunicorn entry point
def create_app():
    return WebServer().app

if __name__ == "__main__":
    # Start the Flask web server in a separate thread
    WebServer().keep_alive()

    # Run the bot loop
    RunBot().run_loop()
