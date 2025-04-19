# You can run main.py directly for development:
#   python main.py
# This will start the bot without the Flask keep-alive server.
# For production or Replit-style keep-alive, use this run.py file.

from flask import Flask
from threading import Thread
from highrise.__main__ import *
import time
import os
from dotenv import load_dotenv
import traceback
import asyncio
from aiohttp.client_exceptions import ClientConnectionError, ClientConnectorError, ClientConnectionResetError

# Load environment variables from .env file
load_dotenv()

class WebServer():
  def __init__(self):
    self.app = Flask(__name__)

    @self.app.route('/')
    def index() -> str:
      return "Alive"

  def run(self) -> None:
    port = int(os.getenv('PORT', 8081))  # Default to 8080 if not set
    self.app.run(
      host='0.0.0.0',
      port=port,
      debug=False,         # Disable debug mode in thread
      use_reloader=False   # Disable reloader in thread
    )

  def keep_alive(self):
    t = Thread(target=self.run)
    t.start()
    RunBot().run_loop()


class RunBot():
  def __init__(self):
    self.definitions = {
      'apiKey': os.getenv('API_KEY'),
      'roomId': os.getenv('ROOM_ID')
    }
    self.reconnect_attempts = 0
    self.max_reconnect_attempts = 10
    self.reconnect_delay = 5  # seconds

  def run_loop(self):
    while True:
      try:
        arun(main(self.definitions))
        # If we reach here, the bot exited cleanly
        print("Bot exited normally. Restarting...")
        time.sleep(1)  # Short delay before restart
        self.reconnect_attempts = 0  # Reset counter on clean exit
      except Exception as e:
        self.reconnect_attempts += 1
        delay = min(self.reconnect_delay * self.reconnect_attempts, 60)  # Cap at 60 seconds
        print(f"Bot crashed with error: {e}")
        traceback.print_exc()
        print(f"Reconnect attempt {self.reconnect_attempts}/{self.max_reconnect_attempts} in {delay} seconds")
        
        if self.reconnect_attempts > self.max_reconnect_attempts:
          print("Maximum reconnection attempts exceeded. Exiting.")
          break
          
        time.sleep(delay)

if __name__ == "__main__":
  WebServer().keep_alive()
