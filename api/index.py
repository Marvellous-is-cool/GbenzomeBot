from flask import Flask, jsonify, request
import os
import threading
import asyncio
from main import Bot
from highrise import *
from highrise.models import *
import time

app = Flask(__name__)

# Global variables to track bot status
bot_instance = None
bot_thread = None
bot_running = False

@app.route('/')
def index():
    return jsonify({
        "status": "alive",
        "bot_running": bot_running,
        "message": "Highrise Bot Server"
    })

@app.route('/start-bot', methods=['POST'])
def start_bot():
    global bot_instance, bot_thread, bot_running
    
    if bot_running:
        return jsonify({"message": "Bot is already running"})
    
    try:
        # Start bot in background thread
        bot_thread = threading.Thread(target=run_bot_async, daemon=True)
        bot_thread.start()
        bot_running = True
        return jsonify({"message": "Bot started successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stop-bot', methods=['POST'])
def stop_bot():
    global bot_running
    bot_running = False
    return jsonify({"message": "Bot stop signal sent"})

@app.route('/status')
def status():
    return jsonify({
        "bot_running": bot_running,
        "thread_alive": bot_thread.is_alive() if bot_thread else False
    })

def run_bot_async():
    global bot_running
    
    api_key = os.getenv('BOT_TOKEN')
    room_id = os.getenv('ROOM_ID')
    
    if not api_key or not room_id:
        print("Missing BOT_TOKEN or ROOM_ID")
        return
    
    try:
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot_instance = Bot()
        definition = BotDefinition(bot_instance, room_id, api_key)
        
        # Run the bot
        loop.run_until_complete(main([definition]))
    except Exception as e:
        print(f"Bot error: {e}")
        bot_running = False

# Auto-start bot when deployed
if __name__ != '__main__':
    # This runs when imported by Vercel
    start_bot()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
