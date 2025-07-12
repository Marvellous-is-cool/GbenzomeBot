# filepath: /Users/mac/Documents/Highrise Bots/Home_boy/functions/emote_catalog.py
# filepath: /Users/mac/Documents/Highrise Bots/Home_boy/functions/emote_catalog.py
from highrise import BaseBot
from highrise.models import User
import asyncio
import json
import os

# Manual list of common emotes in Highrise for fallback
# Updated with comprehensive list of free and premium emotes based on the provided data
MANUAL_EMOTES = {
    "free": ['dance-kawai', 'emote-hyped', 'emoji-halo', 'idle-hero', 'emote-astronaut', 'emote-zombierun', 'emote-dab', 'emote-snake', 'idle-loop-sad', 'idle-loop-happy', 'emote-kissing', 'emoji-shush', 'idle_tough', 'emote-fail3', 'emote-shocked', 'emote-theatrical-test', 'emote-fireworks', 'emote-electrified', 'idle-headless', 'emote-armcannon', 'dance-tiktok4', 'dance-tiktok7', 'dance-tiktok13', 'dance-hiphop', 'emote-hopscotch', 'emote-outfit2', 'emote-pose12', 'emote-fading', 'emote-pose13', 'profile-breakscreen', 'emote-surf', 'emote-cartwheel', 'emote-kissing-passionate', 'dance-tiktok1', 'emote-flirt', 'emote-receive-disappointed', 'emote-gooey', 'emote-oops', 'emote-thief', 'emote-sheephop', 'emote-runhop', 'dance-tiktok15', 'emote-receive-happy', 'dance-tiktok6', 'emote-confused2', 'emote-pose4', 'emote-dinner', 'emote-wavey', 'emote-pose2', 'dance-shuffle', 'emote-twitched', 'emote-juggling', 'idle-dance-tiktok6', 'emote-opera', 'dance-tiktok3', 'dance-kid', 'dance-anime3', 'dance-tiktok16', 'dance-tiktok12', 'dance-tiktok5', 'idle-cold', 'emote-pose11', 'emote-handwalk', 'emote-dramatic', 'emote-outfit', 'sit-chair', 'idle-space', 'mining-mine', 'mining-success', 'mining-fail', 'fishing-pull', 'fishing-idle', 'fishing-cast', 'fishing-pull-small', 'dance-hipshake', 'dance-fruity', 'dance-cheerleader', 'dance-tiktok14', 'emote-looping', 'idle-floating', 'dance-wild', 'emote-howl', 'idle-howl', 'emote-trampoline', 'emote-launch', 'emote-cutesalute', 'emote-salute', 'dance-tiktok11', 'dance-employee', 'emote-gift', 'dance-touch', 'sit-relaxed', 'emote-sleigh', 'emote-attention', 'dance-jinglebell', 'emote-timejump', 'idle-toilet', 'idle-nervous', 'idle-wild', 'emote-iceskating', 'sit-open', 'emote-celebrate', 'emote-shrink', 'emote-pose10', 'emote-shy2', 'emote-puppet', 'emote-headblowup', 'emote-creepycute', 'dance-creepypuppet', 'dance-anime', 'dance-pinguin', 'idle-guitar', 'emote-boxer', 'emote-celebrationstep', 'emote-pose6', 'emote-pose9', 'emote-stargazer', 'dance-wrong', 'idle-uwu', 'emote-fashionista', 'dance-icecream', 'emote-gravity', 'emote-punkguitar', 'idle-dance-tiktok4', 'emote-cutey', 'emote-pose5', 'emote-pose3', 'emote-pose1', 'idle-dance-casual', 'emote-pose8', 'emote-pose7', 'idle-fighter', 'dance-tiktok10', 'idle-dance-tiktok7', 'dance-weird', 'dance-tiktok9', 'emote-cute', 'emote-superpose', 'emote-frog', 'idle_singing', 'emote-energyball', 'emote-maniac', 'emote-swordfight', 'emote-teleporting', 'emote-float', 'emote-telekinesis', 'emote-slap', 'emote-frustrated', 'emote-embarrassed', 'idle-enthusiastic', 'emote-confused', 'dance-shoppingcart', 'emote-rofl', 'emote-roll', 'emote-superrun', 'emote-superpunch', 'emote-kicking', 'emote-apart', 'emote-hug', 'emote-secrethandshake', 'emote-peekaboo', 'emote-monster_fail', 'dance-zombie', 'emote-ropepull', 'emote-proposing', 'emote-sumo', 'emote-charging', 'emote-ninjarun', 'emote-elbowbump', 'idle-angry', 'emote-baseball', 'idle-floorsleeping', 'idle-floorsleeping2', 'emote-hugyourself', 'idle-sad', 'emote-death2', 'emote-levelup', 'idle-posh', 'emote-snowangel', 'emote-hot', 'emote-snowball', 'idle-lookup', 'emote-curtsy', 'dance-russian', 'emote-bow', 'emote-boo', 'emote-fail1', 'emote-fail2', 'emote-jetpack', 'emote-death', 'dance-pennywise', 'idle-sleep', 'idle_layingdown', 'emote-theatrical', 'emote-fainting', 'idle_layingdown2', 'emote-wings', 'emote-laughing2', 'dance-tiktok2', 'emote-model', 'dance-blackpink', 'emoji-sick', 'idle_zombie', 'emote-cold', 'emote-bunnyhop', 'emote-disco', 'dance-sexy', 'emote-heartfingers', 'dance-tiktok8', 'emote-ghost-idle', 'emoji-sneeze', 'emoji-pray', 'emote-handstand', 'dance-smoothwalk', 'dance-singleladies', 'emote-heartshape', 'emoji-naughty', 'emote-deathdrop', 'dance-duckwalk', 'emote-splitsdrop', 'dance-voguehands', 'emoji-give-up', 'emoji-smirking', 'emoji-lying', 'emoji-arrogance', 'emoji-there', 'emoji-poop', 'emoji-hadoken', 'emoji-punch', 'dance-handsup', 'dance-metal', 'dance-orangejustice', 'idle-loop-aerobics', 'idle-loop-annoyed', 'emoji-scared', 'emote-think', 'idle-loop-tired', 'idle-dance-headbobbing', 'emote-disappear', 'emoji-crying', 'idle-loop-tapdance', 'emoji-celebrate', 'emoji-eyeroll', 'emoji-dizzy', 'emoji-gagging', 'emote-greedy', 'emoji-mind-blown', 'emote-shy', 'emoji-clapping', 'emote-hearteyes', 'emote-suckthumb', 'emote-exasperated', 'emote-jumpb', 'emote-exasperatedb', 'emote-peace', 'emote-wave', 'emote-panic', 'emote-harlemshake', 'emote-tapdance', 'emote-gangnam', 'emote-no', 'emote-sad', 'emote-yes', 'emote-kiss', 'emote-gordonshuffle', 'emote-nightfever', 'emote-laughing', 'emote-judochop', 'emote-rainbow', 'emote-robot', 'emote-happy', 'emoji-angry', 'dance-macarena', 'idle-loop-sitfloor', 'emoji-thumbsup', 'emote-tired', 'emote-hello'],
    
    "premium": [
        # Premium emotes
    ]
}

# Define Rarity enum since it's not available in the current version of the library
class Rarity:
    """Custom implementation of Rarity enum to handle missing class in library"""
    NONE = "NONE"
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    EPIC = "EPIC"
    LEGENDARY = "LEGENDARY"
    MYTHIC = "MYTHIC"

# Global dictionaries to store categorized emotes
all_emotes = {}
free_emotes = {}
premium_emotes = {}

# Lists for easier access
all_emotes_list = []
free_emotes_list = []
premium_emotes_list = []

# Numbered shortcuts for quick access
# Will be populated dynamically when emote catalog is loaded
numbered_emotes = {
    # 1: "emote-id-1",
    # 2: "emote-id-2",
    # ...etc.
}

# Top popular emotes to assign to numbers (1-20)
popular_emotes = [
    "emote-kiss", "emote-wave", "emote-laughing", "emote-yes", "emote-no",
    "dance-macarena", "emote-bow", "emote-confused", "emote-sad", "emoji-thumbsup",
    "idle-loop-sitfloor", "emoji-angry", "emote-shy", "dance-tiktok8", "emoji-celebrate",
    "emote-zombierun", "emote-hug", "emote-float", "emote-snowball", "dance-weird"
]

# File to persist emote data to avoid fetching each time
EMOTES_FILE = "emote_catalog.json"

async def fetch_emote_catalog(self: BaseBot):
    """Fetches all emotes from the Highrise API and categorizes them"""
    global all_emotes, free_emotes, premium_emotes
    global all_emotes_list, free_emotes_list, premium_emotes_list

    try:
        # Get all emotes from the API using the category parameter (recommended approach)
        items = None
        try:
            # First approach: Use category="emote" parameter (most accurate)
            print("Attempting to fetch emotes using category parameter...")
            items = await self.webapi.get_items(category="emote", limit=100)
            if items and hasattr(items, 'items'):
                print(f"Found {len(items.items)} emotes using category parameter")
                
                # Check if there are more pages
                total_items = len(items.items)
                last_item_id = items.items[-1].item_id if total_items > 0 else None
                
                # If we have 100 items, there might be more
                while total_items == 100 and last_item_id:
                    print(f"Fetching additional emotes after {last_item_id}...")
                    more_items = await self.webapi.get_items(category="emote", limit=100, starts_after=last_item_id)
                    if more_items and hasattr(more_items, 'items') and len(more_items.items) > 0:
                        items.items.extend(more_items.items)
                        total_items = len(more_items.items)
                        last_item_id = more_items.items[-1].item_id
                        print(f"Retrieved {total_items} more emotes")
                    else:
                        break
                        
                print(f"Total emotes collected using category parameter: {len(items.items)}")
            else:
                # Fallback to our old approach if no items were found
                print("No emotes found using category parameter, falling back to name search")
                return await fetch_emotes_by_name(self)
                
        except Exception as e:
            print(f"Failed to fetch emotes by category: {e}")
            # Fallback to the name search method
            print("Falling back to name search method")
            return await fetch_emotes_by_name(self)
            
        if not items or not hasattr(items, 'items') or len(items.items) == 0:
            print("No emotes found with category parameter, falling back to name search")
            return await fetch_emotes_by_name(self)

        # Reset our emote collections
        all_emotes.clear()
        free_emotes.clear()
        premium_emotes.clear()
        all_emotes_list.clear()
        free_emotes_list.clear()
        premium_emotes_list.clear()

        # Check if we have items and they have the expected structure
        if not hasattr(items, 'items'):
            print("API response doesn't have expected 'items' attribute")
            return False

        # Categorize emotes - filter for emote items only
        emote_count = 0
        for item in items.items:
            # Get item ID with safety check
            emote_id = getattr(item, 'item_id', None)
            if not emote_id:
                continue
                
            # Check if this is an emote by its ID using a more comprehensive pattern
            if not (emote_id.startswith("emote-") or emote_id.startswith("dance-") or 
                    emote_id.startswith("emoji-") or emote_id.startswith("idle") or
                    emote_id.startswith("sit-") or emote_id.startswith("hcc-") or
                    emote_id.startswith("fishing-") or emote_id.startswith("mining-") or
                    emote_id.startswith("profile-") or emote_id.startswith("run-") or
                    emote_id.startswith("walk-") or emote_id.startswith("idle-") or
                    emote_id.startswith("sit_") or emote_id.startswith("idle_")):
                continue
            
            emote_count += 1
            
            # Extract the emote name without the prefix
            emote_name = emote_id.split("-", 1)[-1] if "-" in emote_id else emote_id
            
            # Add to the appropriate category based on whether it's free or premium
            # Safety check for missing attributes
            price = getattr(item, 'price', 0)
            rarity = getattr(item, 'rarity', None)
            item_name = getattr(item, 'item_name', emote_name)
            
            # An emote is free if either price is 0 or rarity is NONE
            is_free = (price == 0) or (str(rarity) == "NONE" or rarity == Rarity.NONE)
            
            emote_info = {
                "id": emote_id,
                "name": emote_name,
                "item_name": getattr(item, 'item_name', emote_name),  # Full name from API if available
                "price": price,
                "is_purchasable": getattr(item, 'is_purchasable', True),
                "rarity": str(rarity) if rarity is not None else "UNKNOWN",
                "is_free": is_free
            }
            
            # Debug output for the first few emotes to help us understand the structure
            if emote_count <= 3:
                print(f"Sample emote data: {emote_id}, Price: {price}, Free: {is_free}")
            
            # Add to general list
            all_emotes[emote_id] = emote_info
            all_emotes_list.append(emote_id)
            
            # Add to appropriate category
            if is_free:
                free_emotes[emote_id] = emote_info
                free_emotes_list.append(emote_id)
            else:
                premium_emotes[emote_id] = emote_info
                premium_emotes_list.append(emote_id)
        
        print(f"Found {emote_count} emote items out of {len(items.items)} total items")

        # Save to file for future use
        save_emote_catalog()

        print(f"Categorized {len(free_emotes_list)} free emotes and {len(premium_emotes_list)} premium emotes")
        return True
    except Exception as e:
        print(f"Error fetching emote catalog: {e}")
        # If we failed to fetch, try to load from file as fallback
        if not all_emotes:
            if os.path.exists(EMOTES_FILE):
                load_emote_catalog()
            
            # If still no emotes, use the manual catalog
            if not all_emotes:
                use_manual_emotes_catalog()
                save_emote_catalog()  # Save for future use
        
        # Even with failures, we at least have the manual catalog
        return len(all_emotes) > 0

def save_emote_catalog():
    """Save the emote catalog to a file"""
    data = {
        "all_emotes": all_emotes,
        "free_emotes": free_emotes,
        "premium_emotes": premium_emotes,
        "all_emotes_list": all_emotes_list,
        "free_emotes_list": free_emotes_list,
        "premium_emotes_list": premium_emotes_list
    }
    
    try:
        with open(EMOTES_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved emote catalog to {EMOTES_FILE} with {len(all_emotes_list)} total emotes")
        print(f"Breakdown: {len(free_emotes_list)} free emotes, {len(premium_emotes_list)} premium emotes")
    except Exception as e:
        print(f"Error saving emote catalog: {e}")

def load_emote_catalog():
    """Load the emote catalog from a file"""
    global all_emotes, free_emotes, premium_emotes
    global all_emotes_list, free_emotes_list, premium_emotes_list
    
    try:
        if os.path.exists(EMOTES_FILE):
            with open(EMOTES_FILE, 'r') as f:
                data = json.load(f)
                
                all_emotes = data.get('all_emotes', {})
                free_emotes = data.get('free_emotes', {})
                premium_emotes = data.get('premium_emotes', {})
                all_emotes_list = data.get('all_emotes_list', [])
                free_emotes_list = data.get('free_emotes_list', [])
                premium_emotes_list = data.get('premium_emotes_list', [])
                
                print(f"Loaded {len(all_emotes)} emotes from {EMOTES_FILE}")
            return True
    except Exception as e:
        print(f"Error loading emote catalog: {e}")
        # Reset to empty collections on error
        all_emotes.clear()
        free_emotes.clear()
        premium_emotes.clear()
        all_emotes_list.clear()
        free_emotes_list.clear()
        premium_emotes_list.clear()
    
    return False

async def get_emote_info(self: BaseBot, emote_id_or_name: str):
    """
    Get detailed information about a specific emote
    
    Args:
        self: The bot instance
        emote_id_or_name: The ID or name of the emote to get info about
        
    Returns:
        A list of formatted messages with emote details
    """
    global all_emotes, all_emotes_list
    
    # If we have no emotes, try to fetch them
    if not all_emotes:
        # Try to load from file first (faster)
        if not load_emote_catalog():
            # If loading fails, fetch from API
            print("No emotes in cache for info lookup, attempting to fetch from API...")
            await fetch_emote_catalog(self)
    
    # If we still have no emotes, use our manual catalog
    if not all_emotes:
        print("No emote catalog available for info lookup, using manual emote catalog")
        use_manual_emotes_catalog()
        save_emote_catalog()  # Save for future use
        
        if not all_emotes:  # If still nothing, give up
            return [f"❌ Failed to load any emote catalog for lookup."]
    
    # Normalize input
    emote_id_or_name = emote_id_or_name.lower()
    
    # First, try to find by exact ID match
    emote_info = all_emotes.get(emote_id_or_name)
    
    # If not found by ID, search by name
    if not emote_info:
        # Search for emotes where name contains the search term
        matches = []
        for emote_id in all_emotes_list:
            info = all_emotes[emote_id]
            name = info["name"].lower()
            item_name = info.get("item_name", "").lower()
            
            # Check for exact matches first
            if name == emote_id_or_name or item_name == emote_id_or_name:
                matches.append((emote_id, 100))  # Exact match gets highest score
            # Then check for partial matches
            elif emote_id_or_name in name or emote_id_or_name in item_name:
                # Give higher score to matches at the beginning
                if name.startswith(emote_id_or_name) or item_name.startswith(emote_id_or_name):
                    matches.append((emote_id, 80))
                else:
                    matches.append((emote_id, 50))
        
        # Sort by score and take the best match
        if matches:
            matches.sort(key=lambda x: x[1], reverse=True)
            best_match_id = matches[0][0]
            emote_info = all_emotes.get(best_match_id)
    
    # If still not found, give up
    if not emote_info:
        return [f"❌ No emote found matching '{emote_id_or_name}'. Try using !emotes search <term>."]
    
    # Format the emote details
    emote_id = emote_info["id"]
    emote_name = emote_info["name"]
    item_name = emote_info.get("item_name", emote_name)
    price = emote_info.get("price", 0)
    is_purchasable = emote_info.get("is_purchasable", True)
    rarity = emote_info.get("rarity", "UNKNOWN")
    is_free = emote_info.get("is_free", True)
    
    # Create a formatted message with all details
    messages = [
        f"📋 Emote Information: {item_name}",
        f"ID: {emote_id}",
        f"Type: {emote_id.split('-')[0] if '-' in emote_id else 'other'}",
        f"Price: {'Free' if is_free else price}",
        f"Purchasable: {'Yes' if is_purchasable else 'No'}",
        f"Rarity: {rarity}",
        f"Usage: !emo {emote_name}"
    ]
    
    # Add alternative similar emotes if available
    if matches and len(matches) > 1:
        similar = [all_emotes[match_id]["name"] for match_id, _ in matches[1:5]]  # Take up to 4 similar emotes
        messages.append(f"Similar emotes: {', '.join(similar)}")
    
    return messages

async def list_emotes(self: BaseBot, category="all", page=1):
    """Generate a formatted string listing the emotes in the specified category"""
    # If we have no emotes, try to fetch them
    if not all_emotes:
        # Try to load from file first (faster)
        if not load_emote_catalog():
            # If loading fails, fetch from API
            print("No emotes in cache, attempting to fetch from API...")
            await fetch_emote_catalog(self)
    
    # If we still have no emotes, use our manual catalog
    if not all_emotes:
        print("No emote catalog available, using manual emote catalog")
        use_manual_emotes_catalog()
        save_emote_catalog()  # Save for future use
        
        if not all_emotes:  # If still nothing, give up
            return ["❌ Failed to load or generate any emote catalog. Please report this issue."]
    
    # Get the appropriate list based on the category
    if category.lower() == "free":
        emote_list = free_emotes_list
        title = "Free Emotes"
    elif category.lower() == "premium":
        emote_list = premium_emotes_list
        title = "Premium Emotes"
    else:  # Default to all
        emote_list = all_emotes_list
        title = "All Emotes"
    
    # Check if we have any emotes in this category
    if not emote_list:
        return [f"No emotes found in the '{category}' category. Try another category."]
    
    # Calculate pagination
    page_size = 15  # Number of emotes per page
    total_pages = max(1, (len(emote_list) + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))  # Ensure page is within bounds
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(emote_list))
    
    # Format the emote list for this page
    current_emotes = emote_list[start_idx:end_idx]
    
    # Generate messages
    messages = [f"🎭 {title} (Page {page}/{total_pages})"]

    # Group emotes by type (e.g., dance, emoji, emote, idle)
    grouped = {}
    for emote_id in current_emotes:
        # Extract the type from the emote_id (e.g., "dance" from "dance-macarena")
        emote_type = emote_id.split("-")[0] if "-" in emote_id else "other"
        emote_name = emote_id.split("-", 1)[-1] if "-" in emote_id else emote_id
        
        if emote_type not in grouped:
            grouped[emote_type] = []
        
        grouped[emote_type].append(emote_name)
    
    # Format each group
    for emote_type, names in grouped.items():
        type_title = emote_type.capitalize()
        msg = f"{type_title}: {', '.join(names)}"
        messages.append(msg)
    
    # Add navigation help
    messages.append(f"Use '!emotes {category} {page+1}' to see the next page.")
    
    return messages

async def search_emote(self: BaseBot, search_term: str, page=1):
    """Search for emotes by name with pagination support and improved matching
    
    Args:
        self: The bot instance
        search_term: The term to search for
        page: The page number to display (defaults to 1)
        
    Returns:
        A list of formatted messages with search results
    """
    global all_emotes, all_emotes_list
    
    # If we have no emotes, try to fetch them
    if not all_emotes:
        # Try to load from file first (faster)
        if not load_emote_catalog():
            # If loading fails, fetch from API
            print("No emotes in cache for search, attempting to fetch from API...")
            await fetch_emote_catalog(self)
    
    # If we still have no emotes, use our manual catalog
    if not all_emotes:
        print("No emote catalog available for search, using manual emote catalog")
        use_manual_emotes_catalog()
        save_emote_catalog()  # Save for future use
        
        if not all_emotes:  # If still nothing, give up
            return [f"❌ Failed to load any emote catalog for searching '{search_term}'."]
    
    search_term = search_term.lower()
    matches = []
    
    # Calculate a match score for each emote
    # Higher score means better match
    for emote_id in all_emotes_list:
        emote_info = all_emotes[emote_id]
        emote_name = emote_info["name"]
        item_name = emote_info.get("item_name", emote_name)
        
        # Initialize match score
        match_score = 0
        
        # Direct match with emote_name gets the highest score
        if search_term == emote_name.lower():
            match_score = 100
        # Direct match with item_name also gets a high score
        elif search_term == item_name.lower():
            match_score = 90
        # Partial match at beginning of emote_name
        elif emote_name.lower().startswith(search_term):
            match_score = 80
        # Partial match at beginning of item_name
        elif item_name.lower().startswith(search_term):
            match_score = 70
        # Partial match anywhere in emote_name
        elif search_term in emote_name.lower():
            match_score = 60
        # Partial match anywhere in item_name
        elif search_term in item_name.lower():
            match_score = 50
        # Words in search term match beginning of words in item_name
        elif any(word in item_name.lower().split() for word in search_term.split()):
            match_score = 40
        # Check for abbreviations (e.g. "tb" matching "thumbs up")
        elif len(search_term) > 1 and all(abbr in item_name.lower() for abbr in search_term):
            match_score = 30
        
        # If we found a match
        if match_score > 0:
            # Add to matches with proper categorization and score for sorting
            category = "Free" if emote_info["is_free"] else "Premium"
            # Get emote type from ID for grouping
            emote_type = emote_id.split("-")[0] if "-" in emote_id else "other"
            matches.append((emote_id, emote_name, category, emote_type, match_score))
    
    # Sort matches by score (highest first)
    matches.sort(key=lambda x: x[4], reverse=True)
    
    # If no matches found
    if not matches:
        return [f"❌ No emotes found matching '{search_term}'"]
    
    # Format the results with pagination
    page_size = 15  # Number of emotes per page
    total_pages = max(1, (len(matches) + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))  # Ensure page is within bounds
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(matches))
    
    # Current page matches
    current_matches = matches[start_idx:end_idx]
    
    # Format header with pagination info
    messages = [f"🔍 Search results for '{search_term}' (Page {page}/{total_pages}, {len(matches)} matches):"]
    
    # Group by type and category
    grouped = {}
    for emote_id, emote_name, category, emote_type, _ in current_matches:
        key = f"{emote_type} ({category})"
        if key not in grouped:
            grouped[key] = []
        
        # Add emote info with ID for reference
        grouped[key].append(f"{emote_name} ({emote_id})")
    
    # Format each group
    for group_name, emotes in grouped.items():
        type_title = group_name.capitalize()
        msg = f"{type_title}: {', '.join(emotes)}"
        messages.append(msg)
    
    # Add navigation help
    if total_pages > 1:
        if page < total_pages:
            messages.append(f"Use '!emotes search {search_term} {page+1}' for the next page.")
        if page > 1: 
            messages.append(f"Use '!emotes search {search_term} {page-1}' for the previous page.")
    
    # Add usage hint
    messages.append(f"Use !emo <name> to perform an emote")
    
    return messages

def use_manual_emotes_catalog():
    """Initialize emote catalog with manually defined emotes if API fails"""
    global all_emotes, free_emotes, premium_emotes
    global all_emotes_list, free_emotes_list, premium_emotes_list
    
    print("Using manually defined emote catalog")
    
    # Clear existing data
    all_emotes.clear()
    free_emotes.clear()
    premium_emotes.clear()
    all_emotes_list.clear()
    free_emotes_list.clear() 
    premium_emotes_list.clear()
    
    # List of GUARANTEED free emotes that all users have access to
    guaranteed_free_emotes = [
        "emote-wave", "emote-yes", "emote-no", "emote-laughing", "emoji-thumbsup", 
        "emoji-angry", "emote-tired", "emote-shy", "emote-confused", "emote-sad",
        "emote-hello", "emoji-clapping", "emoji-crying", "emoji-scared", "emote-think",
        "emoji-sneeze", "emoji-pray", "emoji-ghost", "emoji-poop", "emote-peace",
        "emote-happy", "emoji-celebrate", "idle-loop-sitfloor", "emote-bow", "emote-curtsy",
        "emote-snowball", "emote-hot", "emote-rainbow", "emoji-hadoken", "emoji-punch"
    ]
    
    # Only use the guaranteed free emotes from our list
    for emote_id in guaranteed_free_emotes:
        emote_name = emote_id.split("-", 1)[-1] if "-" in emote_id else emote_id
        emote_info = {
            "id": emote_id,
            "name": emote_name,
            "price": 0,
            "is_purchasable": True,
            "rarity": "NONE",
            "is_free": True
        }
        all_emotes[emote_id] = emote_info
        all_emotes_list.append(emote_id)
        free_emotes[emote_id] = emote_info
        free_emotes_list.append(emote_id)
    
    # Skip premium emotes completely to avoid errors
    
    print(f"Initialized manual emote catalog with {len(free_emotes_list)} guaranteed free emotes")
    return True

async def fetch_emotes_by_name(self: BaseBot):
    """Legacy fallback method to fetch emotes by name prefixes"""
    global all_emotes, free_emotes, premium_emotes
    global all_emotes_list, free_emotes_list, premium_emotes_list
    
    try:
        # Try with item_name parameter to fetch emotes
        # Using common prefixes for emotes to identify them
        print("Attempting to fetch emotes using item_name parameter...")
        items = await self.webapi.get_items(item_name="emote")
        print(f"Found {len(items.items) if items and hasattr(items, 'items') else 0} items with 'emote' in name")
        
        # Create a master list to collect emotes from different searches
        master_items_list = []
        if items and hasattr(items, 'items'):
            master_items_list.extend(items.items)
        
        # Extended list of prefixes to cover more emote types
        prefixes = [
            "dance", "emoji", "idle", "sit", "hcc", "fishing", "mining", "profile", "run", "walk", 
            "emote", "sit-", "idle-", "dance-", "emoji-", "hcc-", "fishing-", "mining-", "profile-"
        ]
        
        # Batch prefixes to avoid too many API calls
        batch_size = 3
        for i in range(0, len(prefixes), batch_size):
            batch = prefixes[i:i+batch_size]
            try:
                for prefix in batch:
                    print(f"Searching for items with prefix: {prefix}")
                    try:
                        prefix_items = await self.webapi.get_items(item_name=prefix)
                        if prefix_items and hasattr(prefix_items, 'items'):
                            print(f"Found {len(prefix_items.items)} items with '{prefix}' in name")
                            master_items_list.extend(prefix_items.items)
                    except Exception as e:
                        print(f"Error searching for {prefix} items: {e}")
                # Add a small delay between batches to prevent rate limiting
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error processing batch with prefixes {batch}: {e}")
        
        # Create a custom response object
        class CustomItems:
            def __init__(self, items_list):
                self.items = items_list
        
        # Deduplicate items by item_id
        unique_items = {}
        for item in master_items_list:
            item_id = getattr(item, 'item_id', None)
            if item_id and item_id not in unique_items:
                unique_items[item_id] = item
        
        # Convert back to list
        unique_items_list = list(unique_items.values())
        
        items = CustomItems(unique_items_list)
        print(f"Total unique emotes collected using name search: {len(unique_items_list)}")
        
        if not unique_items_list:
            print("No emotes found with name search. Falling back to manual catalog.")
            use_manual_emotes_catalog()
            return len(all_emotes) > 0
            
        # Reset our emote collections
        all_emotes.clear()
        free_emotes.clear()
        premium_emotes.clear()
        all_emotes_list.clear()
        free_emotes_list.clear()
        premium_emotes_list.clear()

        # Process items similar to the main fetch method
        emote_count = 0
        for item in items.items:
            # Get item ID with safety check
            emote_id = getattr(item, 'item_id', None)
            if not emote_id:
                continue
                
            # Check if this is an emote by its ID using a more comprehensive pattern
            # Include all common emote prefixes: emote-, dance-, emoji-, idle, sit-, fishing-, mining-, etc.
            if not (emote_id.startswith("emote-") or emote_id.startswith("dance-") or 
                    emote_id.startswith("emoji-") or emote_id.startswith("idle") or
                    emote_id.startswith("sit-") or emote_id.startswith("hcc-") or
                    emote_id.startswith("fishing-") or emote_id.startswith("mining-") or
                    emote_id.startswith("profile-") or emote_id.startswith("run-") or
                    emote_id.startswith("walk-") or emote_id.startswith("idle-") or
                    emote_id.startswith("sit_") or emote_id.startswith("idle_")):
                continue
            
            emote_count += 1
            
            # Extract the emote name without the prefix
            emote_name = emote_id.split("-", 1)[-1] if "-" in emote_id else emote_id
            
            # Add to the appropriate category based on whether it's free or premium
            # Safety check for missing attributes
            price = getattr(item, 'price', 0)
            rarity = getattr(item, 'rarity', None)
            
            # An emote is free if either price is 0 or rarity is NONE
            is_free = (price == 0) or (str(rarity) == "NONE" or rarity == Rarity.NONE)
            
            emote_info = {
                "id": emote_id,
                "name": emote_name,
                "item_name": getattr(item, 'item_name', emote_name),  # Full name from API if available
                "price": price,
                "is_purchasable": getattr(item, 'is_purchasable', True),
                "rarity": str(rarity) if rarity is not None else "UNKNOWN",
                "is_free": is_free
            }
            
            # Debug output for the first few emotes to help us understand the structure
            if emote_count <= 3:
                print(f"Sample emote data: {emote_id}, Price: {price}, Free: {is_free}")
            
            # Add to general list
            all_emotes[emote_id] = emote_info
            all_emotes_list.append(emote_id)
            
            # Add to appropriate category
            if is_free:
                free_emotes[emote_id] = emote_info
                free_emotes_list.append(emote_id)
            else:
                premium_emotes[emote_id] = emote_info
                premium_emotes_list.append(emote_id)
                
        print(f"Found {emote_count} emote items using name search method")
        save_emote_catalog()
        return True
        
    except Exception as e:
        print(f"Error in fetch_emotes_by_name: {e}")
        if not all_emotes:
            # If still no emotes, use the manual catalog
            use_manual_emotes_catalog()
            save_emote_catalog()
        return len(all_emotes) > 0
