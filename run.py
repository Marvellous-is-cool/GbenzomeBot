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
from main import Bot  # Import the Bot class from main.py
import sys
from highrise import *
from highrise.models import *
from highrise.webapi import *
from highrise.models_webapi import *

# Load environment variables from .env file
load_dotenv()
print("Environment loaded - checking variables...")

# Explicitly print found environment variables to debug
print(f"ROOM_ID found: {'Yes' if os.getenv('ROOM_ID') else 'No'}")
print(f"BOT_TOKEN found: {'Yes' if os.getenv('BOT_TOKEN') else 'No'}")

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
    # Use BOT_TOKEN as the API key variable name
    self.api_key = os.getenv('BOT_TOKEN')
    self.room_id = os.getenv('ROOM_ID')
    
    # Validate and print variables for debugging
    print(f"RunBot init - BOT_TOKEN: {'Found' if self.api_key else 'Missing'}")
    print(f"RunBot init - ROOM_ID: {'Found' if self.room_id else 'Missing'}")
    
    if not self.api_key:
        print("ERROR: BOT_TOKEN environment variable is not set!")
        sys.exit(1)
    
    if not self.room_id:
        print("ERROR: ROOM_ID environment variable is not set!")
        sys.exit(1)
        
    print(f"Loaded credentials - Room ID: {self.room_id[:5]}... API Key: {self.api_key[:5]}...")
    
    self.reconnect_attempts = 0
    self.max_reconnect_attempts = 10
    self.reconnect_delay = 5  # seconds

  def run_loop(self):
    while True:
      try:
        # Create a proper BotDefinition object with safer error handling
        print("Initializing bot instance...")
        bot_instance = Bot()
        
        # Log creation of bot definition
        print(f"Creating BotDefinition with room_id: {self.room_id}")
        definition = BotDefinition(bot_instance, self.room_id, self.api_key)
        definitions = [definition]
        
        # More detailed logging
        print("Starting bot with Highrise SDK...")
        arun(main(definitions))
        
        # If we reach here, the bot exited cleanly
        print("Bot exited normally. Restarting...")
        time.sleep(1)  # Short delay before restart
        self.reconnect_attempts = 0  # Reset counter on clean exit
      except TypeError as e:
        print(f"TypeError encountered: {e}")
        print("This might be due to invalid API key or room ID format.")
        traceback.print_exc()
        
        # If we get the specific header serialization error, print more detailed info
        if "Cannot serialize non-str key None" in str(e):
            print("ERROR: Invalid header detected. This may be caused by:")
            print("1. Improperly formatted API key")
            print("2. Improperly formatted room ID")
            print("3. Highrise API changes")
            print(f"Check your .env file to ensure API_KEY and ROOM_ID are properly set.")
            
        # This is a critical error that won't be fixed by retrying
        print("Critical error - exiting...")
        break
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
  # One final explicit check for both variables
  if not os.getenv('BOT_TOKEN'):
    print("ERROR: BOT_TOKEN environment variable is not set!")
    print("Make sure your .env file contains BOT_TOKEN")
    sys.exit(1)
    
  if not os.getenv('ROOM_ID'):
    print("ERROR: ROOM_ID environment variable is not set!")
    print("Make sure your .env file contains ROOM_ID")
    sys.exit(1)
    
  print("Starting web server and bot...")
  WebServer().keep_alive()
