from highrise import *
from highrise.models import *
from highrise.webapi import *
from highrise.models_webapi import *

import asyncio
import random

play_task = None
owner_absent_task = None
soon_task = None
soon_task_lock = asyncio.Lock()
owner_in_room = True
# Add a global variable to track if game is active
game_active = False

comfort_messages = [
    "Don't worry, the host will be right back! 🎲",
    "Bingo will resume soon, stay tuned! 🕒",
    "The game is on pause, but the fun continues! 🎉",
    "Hang tight, the owner will return for more bingo! 🏆",
    "Intermission! The host will be back shortly. 🍀"
]

async def play(self, user, message):
    # --- Fix: resolve user if only user_id is passed ---
    if isinstance(user, str):
        # user is user_id, fetch User object from room
        room_users_resp = await self.highrise.get_room_users()
        user_obj = None
        if hasattr(room_users_resp, "content"):
            for room_user, _ in room_users_resp.content:
                if room_user.id == user:
                    user_obj = room_user
                    break
        user = user_obj
        if user is None:
            await self.highrise.chat("Could not resolve user for !play command.")
            return
    # ---------------------------------------------------

    global play_task, owner_absent_task, soon_task, game_active

    # Only the owner can start the game
    if user.id != self.owner_id:
        await self.highrise.chat("Only the owner can start the game.")
        return

    # Stop any running soon_task
    if soon_task:
        soon_task.cancel()
        soon_task = None

    if play_task and not play_task.done():
        await self.highrise.chat("Game announcements are already running.")
        return

    await self.highrise.chat("Game announcements started! I'll remind everyone every 1 minute.")

    # Set game as active
    game_active = True
    play_task = asyncio.create_task(game_announcement_loop(self))
    owner_absent_task = asyncio.create_task(owner_absent_checker(self))

async def end(self, user, message):
    # --- Fix: resolve user if only user_id is passed ---
    if isinstance(user, str):
        room_users_resp = await self.highrise.get_room_users()
        user_obj = None
        if hasattr(room_users_resp, "content"):
            for room_user, _ in room_users_resp.content:
                if room_user.id == user:
                    user_obj = room_user
                    break
        user = user_obj
        if user is None:
            await self.highrise.chat("Could not resolve user for !end command.")
            return
    # ---------------------------------------------------

    global play_task, owner_absent_task, soon_task, game_active

    # Only the owner can stop the game
    if user.id != self.owner_id:
        await self.highrise.chat("Only the owner can end the game.")
        return

    if play_task:
        play_task.cancel()
        play_task = None
    if owner_absent_task:
        owner_absent_task.cancel()
        owner_absent_task = None
    if soon_task:
        soon_task.cancel()
        soon_task = None

    # Set game as inactive
    game_active = False
    await self.highrise.chat("Game announcements stopped.")

async def soon(self, user, message):
    # --- Fix: resolve user if only user_id is passed ---
    if isinstance(user, str):
        room_users_resp = await self.highrise.get_room_users()
        user_obj = None
        if hasattr(room_users_resp, "content"):
            for room_user, _ in room_users_resp.content:
                if room_user.id == user:
                    user_obj = room_user
                    break
        user = user_obj
        if user is None:
            await self.highrise.chat("Could not resolve user for !soon command.")
            return
    # ---------------------------------------------------

    global play_task, soon_task, soon_task_lock

    # Only the owner can use !soon
    if user.id != self.owner_id:
        await self.highrise.chat("Only the owner can use !soon.")
        return

    if play_task and not play_task.done():
        await self.highrise.chat("You cannot use !soon while !play is running.")
        return

    # Parse minutes from message
    parts = message.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await self.highrise.chat("Usage: !soon <minutes>")
        return
    minutes = int(parts[1])
    if minutes < 1:
        await self.highrise.chat("Please specify a positive number of minutes.")
        return

    # Use a lock to prevent race conditions with soon_task
    async with soon_task_lock:
        # Cancel any previous soon_task
        if soon_task:
            soon_task.cancel()
            soon_task = None

        soon_task = asyncio.create_task(soon_countdown(self, user, minutes))

async def game_announcement_loop(self):
    try:
        while True:
            await self.highrise.chat("The game has started downstairs, please watch")
            await asyncio.sleep(60)  # 1 minute
    except asyncio.CancelledError:
        pass

async def soon_countdown(self, user, minutes):
    global soon_task, game_active
    try:
        total_seconds = minutes * 60
        while total_seconds > 0:
            # Show minutes if more than 60 seconds, else show seconds
            if total_seconds > 60:
                mins = total_seconds // 60
                await self.highrise.chat(f"Bingo game starts in {mins} minute{'s' if mins > 1 else ''}!")
                sleep_time = 60
            elif total_seconds == 60:
                await self.highrise.chat("Bingo game starts in 1 minute!")
                sleep_time = 1
            else:
                await self.highrise.chat(f"Bingo game starts in {total_seconds} seconds!")
                sleep_time = 1
            await asyncio.sleep(sleep_time)
            total_seconds -= sleep_time
        
        # When countdown reaches zero, automatically start the game
        await self.highrise.chat("Bingo game is starting now!")
        # Call play function directly with the user who started the countdown
        await play(self, user, "!play")
    except asyncio.CancelledError:
        await self.highrise.chat("Countdown cancelled.")
    finally:
        # Ensure soon_task is cleared when finished or cancelled
        global soon_task_lock
        async with soon_task_lock:
            soon_task = None

async def owner_absent_checker(self):
    global owner_in_room
    try:
        while True:
            # Check if owner is in the room
            room_users_resp = await self.highrise.get_room_users()
            if hasattr(room_users_resp, "content"):
                owner_in_room = any(
                    room_user.id == self.owner_id for room_user, _ in room_users_resp.content
                )
            else:
                owner_in_room = False

            if not owner_in_room:
                # Send a random comfort message
                await self.highrise.chat(random.choice(comfort_messages))
                await asyncio.sleep(120)  # Check every 2 minutes
            else:
                await asyncio.sleep(30)  # Check more frequently if owner is present
    except asyncio.CancelledError:
        pass

# Function to check if game is active (for main.py to use)
def is_game_active():
    return game_active
