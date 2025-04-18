from highrise import *
from highrise.models import *
from highrise.webapi import *
from highrise.models_webapi import *

import asyncio
import random

# Store the periodic task and state globally
play_task = None
owner_absent_task = None
owner_in_room = True

comfort_messages = [
    "Don't worry, the host will be right back! 🎲",
    "Bingo will resume soon, stay tuned! 🕒",
    "The game is on pause, but the fun continues! 🎉",
    "Hang tight, the owner will return for more bingo! 🏆",
    "Intermission! The host will be back shortly. 🍀"
]

async def play(self, user, message):
    global play_task, owner_absent_task, owner_in_room

    # Only the owner can start the game
    if user.id != self.owner_id:
        await self.highrise.chat("Only the owner can start the game.")
        return

    if play_task and not play_task.done():
        await self.highrise.chat("Game announcements are already running.")
        return

    await self.highrise.chat("Game announcements started! I'll remind everyone every 5 minutes.")

    play_task = asyncio.create_task(game_announcement_loop(self))
    owner_absent_task = asyncio.create_task(owner_absent_checker(self))

async def end(self, user, message):
    global play_task, owner_absent_task

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

    await self.highrise.chat("Game announcements stopped.")

async def game_announcement_loop(self):
    try:
        while True:
            await self.highrise.chat("The game has started downstairs, please watch")
            await asyncio.sleep(300)  # 5 minutes
    except asyncio.CancelledError:
        pass

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
