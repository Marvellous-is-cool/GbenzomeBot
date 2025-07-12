import asyncio
import os
import sys
import time
import traceback
import json
from typing import List, Dict, Any, Callable, Awaitable

from dotenv import load_dotenv
import uvicorn

from highrise import BaseBot
from highrise.__main__ import BotDefinition, main
from main import Bot  # Import the Bot class from main.py

# Load environment variables from .env file
load_dotenv()

# Global variable to track the bot task
bot_task = None
bot_running = False

class BotRunner:
    def __init__(self):
        # Use BOT_TOKEN as the API key variable name
        self.api_key = os.getenv('BOT_TOKEN')
        self.room_id = os.getenv('ROOM_ID')
        
        # Validate environment variables
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
        self._running = False

    async def run_bot(self):
        """Run the bot with reconnection logic"""
        self._running = True
        while self._running:
            try:
                # Create a proper BotDefinition object
                print("Initializing bot instance...")
                bot_instance = Bot()
                
                # Log creation of bot definition
                print(f"Creating BotDefinition with room_id: {self.room_id}")
                definition = BotDefinition(bot_instance, self.room_id, self.api_key)
                definitions = [definition]
                
                # Start the bot
                print("Starting bot with Highrise SDK...")
                await main(definitions)
                
                # If we reach here, the bot exited cleanly
                print("Bot exited normally. Restarting...")
                await asyncio.sleep(1)  # Short delay before restart
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
                    
                await asyncio.sleep(delay)
        
        self._running = False
        print("Bot runner stopped")
    
    def stop(self):
        """Stop the bot gracefully"""
        self._running = False

# Initialize the bot runner
runner = BotRunner()

# Simple ASGI web app without FastAPI
async def app_lifespan():
    # Start the bot in the background
    global bot_task, bot_running
    if not bot_running:
        bot_task = asyncio.create_task(runner.run_bot())
        bot_running = True
    try:
        # Keep the lifespan running until shutdown
        while True:
            await asyncio.sleep(60)  # Just keep alive
    except asyncio.CancelledError:
        # Stop the bot when the app shuts down
        if bot_running and bot_task:
            runner.stop()
            if not bot_task.done():
                bot_task.cancel()
            bot_running = False
        raise

# Create a simple ASGI application for health check endpoints
async def app(scope, receive, send):
    assert scope['type'] == 'http'
    
    # Start lifespan if this is the first request
    global bot_task, bot_running
    if not bot_running:
        asyncio.create_task(app_lifespan())

    # Parse path for routing
    path = scope['path']
    
    # Simple router
    if path == '/':
        # Root endpoint - health check
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/html'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'<html><body><h1>Highrise Bot is Running</h1><p>Status: ' + 
                   (b'Active' if bot_running else b'Inactive') + 
                   b'</p></body></html>',
        })
    
    elif path == '/status':
        # Status endpoint - JSON response
        status_data = {
            'bot_running': bot_running,
            'reconnect_attempts': runner.reconnect_attempts,
            'max_reconnect_attempts': runner.max_reconnect_attempts
        }
        
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'application/json'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(status_data).encode('utf-8'),
        })
    
    else:
        # Not found
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Not Found',
        })

# This allows running the file with python directly (for development)
# or using it as an ASGI application with Uvicorn
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting Uvicorn server on port {port}...")
    uvicorn.run("asgi:app", host="0.0.0.0", port=port, reload=True)
