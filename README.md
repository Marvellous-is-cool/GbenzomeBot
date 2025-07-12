# Home_boy - Highrise Bot

A feature-rich Highrise bot designed to host Bingo games, manage emotes, and facilitate interactive experiences in a Highrise room. This bot combines utility features with entertainment capabilities to create an engaging user experience.

## Features

### Bingo Game Management

- Start/stop bingo game announcements with `!play` and `!end` commands
- Schedule upcoming games with the `!soon <minutes>` command
- Automatic welcome messages that inform users about active games
- Bot provides comfort messages when the room owner is absent

### User Interaction

- Emotes and actions triggered by simple commands
- Social interaction commands (`!fight`, `!hug`, `!flirt`) for users to interact with each other
- Custom welcome messages for room visitors
- Loop emotes on yourself or other users with `!loop <emote> [username]`
- Dynamic emote catalog system with automatic categorization of free and premium emotes
- Search for emotes by name with `!search <name>`
- Browse emotes by category with `!emotes free` or `!emotes premium`

### Room Management

- VIP system with special permissions
- Teleportation commands for authorized users
- Position control for moving users to specific locations
- Tip tracking system to record and display top tippers
- Room moderation with kick functionality

### Avatar Customization

- Equip/remove various clothing and accessory items
- Comprehensive lists of available items by category
- Easy-to-use commands for bot appearance management

### Music Request System

- Request songs with `!request <song name or URL>`
- View the queue with `!queue` or `!q`
- See the currently playing song with `!np` or `!nowplaying`
- Like the current song with `!like`
- VIPs and the room owner can skip songs with `!skip` or clear the queue with `!clear`
- Song history and queue persistence between bot restarts

### System Features

- Error handling and connection retry mechanisms
- Persistent data storage in data.json
- Web server for keeping the bot alive

## Commands Overview

### General User Commands

- `!allemo` or `!emotes` - List all available emotes (paginated)
- `!emotes free` - Show only free emotes
- `!emotes premium` - Show only premium emotes
- `!search <name>` - Search for emotes by name
- `!emo` - Get a random emote suggestion
- `!emote <target> <emote>` - Send emote to a specific user
- `!fight @username` - Initiate a sword fight with another user
- `!hug @username` - Hug another user
- `!flirt @username` - Flirt with another user
- `!loop <emote>` - Loop an emote on yourself
- `!request <song>` - Request a song to be played
- `!queue` or `!q` - View the current song queue
- `!np` or `!nowplaying` - See what song is currently playing
- `!like` - Like the currently playing song
- `!stop` - Stop any current emote loop on yourself
- `!door` - Teleport to the door/entrance position

### VIP Commands

- `!teleport <username> <x,y,z>` - Teleport a user to specific coordinates
- `!pos <username>` - Move a user to a predefined position
- `!tele host` - Teleport to the host platform
- `!refresh` - Manually refresh the emote catalog from Highrise API
- `!skip` - Skip the current song in the queue

### Owner Commands

- `!set` - Set the bot's position to your current location
- `!top` - Show top 10 tippers
- `!get <username>` - Get a specific user's tip amount
- `!wallet` - Check bot's current gold balance
- `!addvip <username>` - Add a user to VIP list
- `!kick <username>` - Kick a user from the room
- `!equip <item name>` - Equip an item on the bot
- `!remove <category>` - Remove an item category from the bot

### Bingo Game Commands (Owner only)

- `!play` - Start bingo game announcements
- `!end` - End bingo game announcements
- `!soon <minutes>` - Announce upcoming game and start countdown

## Message Commands

Send these commands in DM to the bot for additional information and functionality:

- `help` - Get general help information
- `commands` - List available commands
- `bot commands` - Show owner-only bot management commands
- `categories` - List item categories for the `!remove` command
- `eq h/t/p/s/b/so/a/fh/eb/e/n/m/fr` - Lists of specific item categories (Hair, Tops, Pants, etc.)

## Setup Instructions

1. Create a `.env` file with the following variables:

   ```
   PORT=8000
   ROOM_ID=your_room_id
   BOT_TOKEN=your_bot_token
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Bot

There are several ways to run the Home_boy bot:

### Option 1: Direct Python (Development)

```bash
python main.py
```

This starts the bot directly without any web server (good for local testing).

### Option 2: Flask Web Server (Previous method)

```bash
python run.py
```

This starts the bot with a Flask web server for a keep-alive mechanism.

### Option 3: Uvicorn ASGI Server (Recommended)

```bash
uvicorn asgi:app --host 0.0.0.0 --port 8000
```

This runs the bot with Uvicorn, which provides better performance and async capabilities.

For production use with automatic reloading:

```bash
uvicorn asgi:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

When using the ASGI/Uvicorn server, these REST endpoints become available:

- `GET /` - Check if the bot is running
- `GET /status` - Get detailed bot status
- `POST /restart` - Restart the bot

  ```

  ```

3. Run the bot:

   ```bash
   # For development (without web server)
   python main.py

   # For production with web server
   python run.py
   ```

## Files and Structure

- `main.py` - Main bot implementation
- `run.py` - Bot runner with web server for keeping alive
- `loop_emote.py` - Emote looping functionality
- `getItems.py` - Item data and helper functions
- `connection_helper.py` - Network connection retry helpers
- `data.json` - Data storage for bot position and user tips
- `functions/` - Command modules for various bot features
  - `allemo.py` - All emotes command
  - `emo.py` - Random emote command
  - `emote.py` - Targeted emote command
  - `equip.py` - Avatar customization
  - `play.py` - Bingo game management
  - `remove.py` - Item removal
  - `userinfo.py` - User information display

## Authors

- @coolbuoy - Original creator and maintainer

## Contributing

Feel free to fork this repository and submit pull requests for new features or bug fixes.

## License

This project is available for personal use.
