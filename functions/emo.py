from highrise import BaseBot
from highrise.models import User
import re, random
from functions.emote_catalog import all_emotes, all_emotes_list, free_emotes_list
from functions.numbered_emotes import get_emote_by_number, format_numbered_emotes, initialize_numbered_emotes

# Legacy list for fallback (kept for backward compatibility)
emoteshelp = [
    "kiss", "no", "sad", "yes", "laughing", "hello", "wave", "shy", "tired", 
    "angry", "sitfloor", "thumbsup", "lust", "cursing", "greedy", "flex", 
    "gagging", "celebrate", "macarena", "tiktok8", "blackpink", "model", 
    "tiktok2", "pennywise", "bow", "russian", "curtsy", "snowball", "hot", 
    "snowangel", "charging", "shoppingcart", "confused", "enthusiastic", 
    "telekinesis", "float", "teleporting", "swordfight", "maniac", 
    "energyball", "snake", "idle_singing", "frog", "superpose", "cute", 
    "tiktok9", "weird", "tiktok10", "pose7", "pose8", "casual", "pose1", 
    "pose3", "pose5", "cutey", "punkguitar", "zombierun", "fashionista", 
    "gravity", "icecream", "wrong", "uwu", "tiktok4"
]


async def emo(self: BaseBot, user: User, message: str) -> None:
    """
    Handle emote commands with improved support for:
    - Number-based shortcuts (e.g., !emo 1)
    - Emote names without prefixes (e.g., !emo kiss)
    - Full emote IDs (e.g., !emo emote-kiss)
    - Last word handling (e.g., !emo cast for fishing-cast)
    """
    # Get the numbered emotes
    numbered_emotes = initialize_numbered_emotes()
    
    parts = message.strip().split()
    
    if len(parts) < 2:
        # If no parameters, suggest a random emote
        random_emote = random.choice(emoteshelp)
        await self.highrise.chat(f"Try saying an emote name like '{random_emote}' or a number from 1-30")
        return
    
    # Get the parameter (either a number or emote name)
    param = parts[1].lower()
    emote_id = None
    
    # Check if this is a number
    if param.isdigit():
        emote_id = get_emote_by_number(param)
        if not emote_id:
            await self.highrise.chat(f"Invalid emote number: {param}. Use !numbers to see available numbered emotes.")
            return
    else:
        # Not a number, treat as emote name
        # Check if the name is a full emote ID already
        if param in all_emotes:
            emote_id = param
        else:
            # Try to find the emote by name in the catalog
            matches = []
            
            # First, check for exact matches
            for eid in all_emotes_list:
                emote_name = eid.split('-', 1)[-1] if '-' in eid else eid
                
                # Exact match gets highest score
                if param == emote_name.lower():
                    matches.append((eid, 100))
                # Start with match gets high score
                elif emote_name.lower().startswith(param):
                    matches.append((eid, 80))
                # Contains match gets medium score  
                elif param in emote_name.lower():
                    matches.append((eid, 60))
                # Last word match for cases like "cast" for "fishing-cast"
                elif param == eid.split('-')[-1].lower():
                    matches.append((eid, 90))
            
            # If we found matches, use the best one
            if matches:
                matches.sort(key=lambda x: x[1], reverse=True)
                emote_id = matches[0][0]
    
    # If we found an emote, perform it
    if emote_id:
        try:
            # Double-check if this is a numbered emote (these should be guaranteed to work)
            is_numbered_emote = False
            for num, num_emote_id in numbered_emotes.items():
                if emote_id == num_emote_id:
                    is_numbered_emote = True
                    break
            
            # For non-numbered emotes, be extra cautious
            if not is_numbered_emote:
                is_free_emote = False
                
                # Check if it's in our predefined list of free emotes
                if emote_id in free_emotes_list:
                    is_free_emote = True
                # Check if it follows the naming convention of GUARANTEED free emotes
                # We're very selective here - only basic emotes from our verified list
                elif emote_id in [
                    "emote-wave", "emote-yes", "emote-no", "emote-laughing", "emoji-thumbsup", 
                    "emoji-angry", "emote-tired", "emote-shy", "emote-confused", "emote-sad",
                    "emote-hello", "emoji-clapping", "emoji-crying", "emoji-scared", "emote-think",
                    "emoji-sneeze", "emoji-pray", "emoji-ghost", "emoji-poop", "emote-peace",
                    "emote-happy", "emoji-celebrate", "idle-loop-sitfloor", "emote-bow", "emote-curtsy"
                ]:
                    is_free_emote = True
                    
                if not is_free_emote:
                    # For non-free emotes, use a guaranteed fallback without notifying the user
                    # (to avoid spamming chat with error messages)
                    emote_id = "emote-wave"  # Most reliable fallback
            
            # Try to perform the emote
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except Exception:
                # If the first attempt fails, silently try the most reliable emote
                try:
                    await self.highrise.send_emote("emote-wave", user.id)
                except Exception:
                    # Last resort - try an absolute basic emote
                    try:
                        await self.highrise.send_emote("emoji-thumbsup", user.id)
                    except Exception:
                        # If all attempts fail, just silently fail to avoid spamming errors
                        pass
            
        except Exception:
            # Outer exception handler as a safety net
            # Silent fallback - don't announce errors to avoid chat spam
            pass
    else:
        await self.highrise.chat(f"Emote '{param}' not found. Try using !emotes search <term> or !numbers to see available emotes.")


async def numbers(self: BaseBot, user: User, message: str) -> None:
    """Display numbered emote shortcuts"""
    # Check if we need to reinitialize the numbered emotes
    initialize_numbered_emotes()
    
    parts = message.strip().split()
    page = 1
    
    # Check if page number is specified
    if len(parts) > 1 and parts[1].isdigit():
        page = int(parts[1])
    
    # Get the formatted list
    messages = format_numbered_emotes(page)
    
    # Send each message
    for msg in messages:
        await self.highrise.chat(msg)