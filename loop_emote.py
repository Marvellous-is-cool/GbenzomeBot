import asyncio
import re

# Dictionary to store user tasks
user_tasks = {}

# Import emote catalog functions
import os
import sys
# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from functions.emote_catalog import load_emote_catalog, use_manual_emotes_catalog, all_emotes_list, all_emotes

# Initialize emote catalog (will be updated at runtime)
if not load_emote_catalog():
    use_manual_emotes_catalog()

# Function to find emote ID by name
def find_emote_by_name(emote_name):
    """
    Find an emote ID by name - will do partial matching and handle approximate names
    
    Returns:
        An emote ID if found, None otherwise
    """
    emote_name = emote_name.lower()
    matches = []
    
    # Check for exact ID match first
    if emote_name in all_emotes:
        return emote_name
        
    # Check for exact name match
    for emote_id in all_emotes_list:
        info = all_emotes[emote_id]
        name = info["name"].lower()
        item_name = info.get("item_name", "").lower()
        
        # Exact match
        if emote_name == name:
            return emote_id
            
        # Start with best partial matches
        if name.startswith(emote_name) or item_name.startswith(emote_name):
            matches.append((emote_id, 80))
        elif emote_name in name or emote_name in item_name:
            matches.append((emote_id, 50))
    
    if matches:
        # Sort by score and return best match
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0][0]
    
    return None

async def send_specific_emote_periodically(self, user, emote_name, target_user=None):
    """
    If target_user is None, loop emote for 'user'.
    If target_user is provided, loop emote for 'target_user'.
    """
    try:
        # Determine the username for task tracking
        task_user = target_user if target_user else user

        # Check if there's an existing task for the user and cancel it
        existing_task = user_tasks.get(task_user.username)
        if existing_task:
            existing_task.cancel()
            await self.highrise.chat(f"Stopping previous emote task for {task_user.username}!")

        # Use regular expression to find the emote name in the user's input
        # Allow complex emote names including hyphens and underscores
        emote_match = re.match(r'^[\w-_]+$', emote_name)
        if not emote_match:
            await self.highrise.chat(f"Invalid emote name format: {emote_name}. Stopping.")
            return

        provided_emote_name = emote_name.lower()

        # Find the emote ID in our catalog
        emote_id = find_emote_by_name(provided_emote_name)
        
        if not emote_id:
            await self.highrise.chat(f"Emote '{provided_emote_name}' not found in the catalog. Use !emotes search to find available emotes.")
            return

        # Create a new task for the user
        task = asyncio.create_task(send_emote_periodically(self, task_user, provided_emote_name, emote_id))
        user_tasks[task_user.username] = task

    except Exception as e:
        await self.highrise.chat(f"Error setting up emote task: {str(e)}")

async def send_emote_periodically(self, user, emote_name, emote_id):
    """Send an emote repeatedly until cancelled or user leaves"""
    try:
        # Initial success notification
        await self.highrise.chat(f"🎭 Starting emote loop with '{emote_name}' for {user.username}...")
        
        loop_count = 0
        while True:
            # Check if user is still in room
            user_in_room = await is_user_in_room(self, user)
            if not user_in_room:
                await self.highrise.chat(f"User {user.username} left the room. Stopping emote loop.")
                # Clean up the task dictionary
                if user.username in user_tasks:
                    del user_tasks[user.username]
                return

            # Send the emote
            try:
                await self.highrise.send_emote(emote_id, user.id)
                loop_count += 1
                
                # Every 10 loops, send a status message
                if loop_count % 10 == 0:
                    await self.highrise.chat(f"🔄 Still running '{emote_name}' for {user.username} ({loop_count} loops)")
                    
                # Wait before sending again
                await asyncio.sleep(2)  # 2-second delay between emotes
                
            except Exception as e:
                await self.highrise.chat(f"Error sending emote: {str(e)}")
                if user.username in user_tasks:
                    del user_tasks[user.username]
                return
                
    except asyncio.CancelledError:
        # Clean up when task is cancelled
        if user.username in user_tasks:
            del user_tasks[user.username]
        # We don't need to do anything else as this is expected behavior
        
    except Exception as e:
        await self.highrise.chat(f"Emote loop error: {str(e)}")
        if user.username in user_tasks:
            del user_tasks[user.username]

async def is_user_in_room(self, user):
    """Check if a user is in the current room"""
    try:
        room_users = await self.highrise.get_room_users()
        return any(room_user.id == user.id for room_user, _ in room_users.content)
    except Exception as e:
        print(f"Error checking if user in room: {e}")
        # Default to True to prevent unnecessary task termination
        return True

async def stop_emote_task(self, user):
    """Stop the emote task for the specified user"""
    existing_task = user_tasks.get(user.username)
    if existing_task:
        existing_task.cancel()
        # We can remove it from the dictionary here or let the task clean up
        if user.username in user_tasks:
            del user_tasks[user.username]
        await self.highrise.chat(f"Stopped your emote task, {user.username}!")
    else:
        await self.highrise.chat(f"No active emote task to stop, {user.username}!")

async def stop_emote_task_by_username(self, username):
    """Stop an emote task using just the username (for admin commands)"""
    existing_task = user_tasks.get(username)
    if existing_task:
        existing_task.cancel()
        if username in user_tasks:
            del user_tasks[username]
        await self.highrise.chat(f"Stopped emote task for {username}!")
    else:
        await self.highrise.chat(f"No active emote task to stop for {username}!")

async def list_active_tasks(self):
    """List all currently active emote tasks"""
    if not user_tasks:
        await self.highrise.chat("No active emote tasks running.")
        return
        
    await self.highrise.chat(f"🎭 Active Emote Tasks ({len(user_tasks)}):")
    for username in user_tasks:
        await self.highrise.chat(f"- {username}")
