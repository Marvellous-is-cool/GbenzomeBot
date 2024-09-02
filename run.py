from flask import Flask
from threading import Thread
from highrise.__main__ import *
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WebServer():
  def __init__(self):
    self.app = Flask(__name__)

    @self.app.route('/')
    def index() -> str:
      return "Alive"

  def run(self) -> None:
    port = int(os.getenv('PORT', 8080))  # Default to 8080 if not set
    self.app.run(host='0.0.0.0', port=port)

  def keep_alive(self):
    t = Thread(target=self.run)
    t.start()


class RunBot():
  def __init__(self) -> None:
    self.room_id = os.getenv('ROOM_ID')
    self.bot_token = os.getenv('BOT_TOKEN')
    self.bot_file = "main"
    self.bot_class = "Bot"

    self.definitions = [
        BotDefinition(
            getattr(import_module(self.bot_file), self.bot_class)(),
            self.room_id, self.bot_token)
    ]  # More BotDefinition classes can be added to the definitions list

  def run_loop(self) -> None:
    while True:
      try:
        arun(main(self.definitions))

      except Exception as e:
        print("Error: ", e)
        time.sleep(5)


if __name__ == "__main__":
  WebServer().keep_alive()
  RunBot().run_loop()
