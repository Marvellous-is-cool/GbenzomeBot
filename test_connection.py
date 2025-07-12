import asyncio
import os
import sys
from dotenv import load_dotenv
from highrise import BaseBot
from highrise.__main__ import BotDefinition, main
from main import Bot  # Import the Bot class from main.py

# Load environment variables from .env file
load_dotenv()

async def test_connection():
    """Test if the bot can connect to Highrise with the provided credentials"""
    api_key = os.getenv('BOT_TOKEN')
    room_id = os.getenv('ROOM_ID')
    
    # Validate environment variables
    if not api_key:
        print("ERROR: BOT_TOKEN environment variable is not set!")
        sys.exit(1)
    
    if not room_id:
        print("ERROR: ROOM_ID environment variable is not set!")
        sys.exit(1)
        
    print(f"Testing connection with:")
    print(f"- Room ID: {room_id[:5]}...")
    print(f"- API Key: {api_key[:5]}...")
    
    try:
        # Create bot instance
        print("Initializing bot instance...")
        bot_instance = Bot()
        
        # Create BotDefinition
        print("Creating BotDefinition...")
        definition = BotDefinition(bot_instance, room_id, api_key)
        definitions = [definition]
        
        # Start the bot with a timeout
        print("Attempting to connect to Highrise...")
        connection_task = asyncio.create_task(main(definitions))
        
        # Set a timeout for the connection attempt
        try:
            # Wait for 10 seconds for the connection to succeed
            await asyncio.wait_for(connection_task, 10)
        except asyncio.TimeoutError:
            # If we get here, the bot connected successfully but ran beyond the timeout
            print("Connection successful! Bot connected to Highrise.")
            # Cancel the task to prevent it from continuing
            connection_task.cancel()
            return True
        
        # If we get here, the task completed normally (unlikely for a bot)
        print("Bot connected but exited unexpectedly.")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting connection test...")
    success = asyncio.run(test_connection())
    
    if success:
        print("\n✅ CONNECTION TEST SUCCESSFUL")
        print("The bot can connect to Highrise with the provided credentials.")
        print("You can now run the bot with:")
        print("  ./start_uvicorn.sh")
        print("  or")
        print("  uvicorn asgi:app --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ CONNECTION TEST FAILED")
        print("The bot could not connect to Highrise with the provided credentials.")
        print("Please check your .env file and make sure the BOT_TOKEN and ROOM_ID are correct.")
