from highrise import BaseBot
from highrise.models import User
from functions.emote_catalog import all_emotes, all_emotes_list, free_emotes_list

# Default list of GUARANTEED FREE emotes to assign to numbers (1-30)
# These are basic emotes that every user has access to
POPULAR_EMOTES = [
    "emote-wave", "emote-yes", "emote-no", "emote-laughing", "emoji-thumbsup", 
    "emoji-angry", "emote-tired", "emote-shy", "emote-confused", "emote-sad",
    "emote-hello", "emoji-clapping", "emoji-crying", "emoji-scared", "emote-think",
    "emoji-sneeze", "emoji-pray", "emoji-ghost", "emoji-poop", "emote-peace",
    "emote-happy", "emoji-celebrate", "idle-loop-sitfloor", "emote-bow", "emote-curtsy",
    "emote-snowball", "emote-hot", "emote-rainbow", "emoji-hadoken", "emoji-punch"
]

# Dictionary to store the number-to-emote mapping
numbered_emotes = {}

def initialize_numbered_emotes():
    """Initialize the numbered emotes dictionary with popular emotes"""
    global numbered_emotes, POPULAR_EMOTES
    
    # Reset the dictionary
    numbered_emotes.clear()
    
    # SAFE APPROACH: Use ONLY the guaranteed free emotes from our curated list
    # These are basic emotes that every Highrise user has access to
    for i, emote_id in enumerate(POPULAR_EMOTES, 1):
        if i > 30:  # Limit to 30 numbered shortcuts
            break
        numbered_emotes[str(i)] = emote_id
    
    # If we somehow don't have enough emotes, use a small subset of guaranteed free ones
    if len(numbered_emotes) < 30:
        # These are absolutely guaranteed to be available to everyone
        basic_emotes = ["emote-wave", "emote-yes", "emote-no", "emoji-thumbsup", "emoji-angry"]
        
        # Fill in any remaining slots
        for i in range(len(numbered_emotes) + 1, 31):
            if i - len(numbered_emotes) <= len(basic_emotes):
                idx = (i - len(numbered_emotes) - 1) % len(basic_emotes)
                if basic_emotes[idx] not in numbered_emotes.values():
                    numbered_emotes[str(i)] = basic_emotes[idx]
    
    print(f"Initialized {len(numbered_emotes)} numbered emotes")
    
    return numbered_emotes

def get_emote_by_number(number: str):
    """Get an emote ID by its number shortcut"""
    # Make sure numbered_emotes is initialized
    if not numbered_emotes:
        initialize_numbered_emotes()
    
    return numbered_emotes.get(number, None)

def get_numbered_emotes_list():
    """Return a formatted list of all numbered emotes"""
    if not numbered_emotes:
        initialize_numbered_emotes()
    
    result = []
    for num, emote_id in numbered_emotes.items():
        emote_name = emote_id.split('-', 1)[-1] if '-' in emote_id else emote_id
        result.append(f"{num}: {emote_name}")
    
    return result

def format_numbered_emotes(page=1, page_size=10):
    """Format numbered emotes into pages for display"""
    if not numbered_emotes:
        initialize_numbered_emotes()
    
    # Calculate pagination
    total_items = len(numbered_emotes)
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_items)
    
    # Get items for the current page
    current_items = list(numbered_emotes.items())[start_idx:end_idx]
    
    # Format the results
    messages = [f"🔢 Numbered Emote Shortcuts (Page {page}/{total_pages}):"]
    
    # Group by type
    grouped = {}
    for num, emote_id in current_items:
        emote_type = emote_id.split('-')[0] if '-' in emote_id else 'other'
        emote_name = emote_id.split('-', 1)[-1] if '-' in emote_id else emote_id
        
        if emote_type not in grouped:
            grouped[emote_type] = []
        
        grouped[emote_type].append(f"{num}: {emote_name}")
    
    # Format each group
    for type_name, items in grouped.items():
        type_title = type_name.capitalize()
        messages.append(f"{type_title}: {', '.join(items)}")
    
    # Add navigation help
    if total_pages > 1:
        messages.append(f"Use '!numbers {page+1}' to see the next page.")
    
    # Add usage instructions
    messages.append("To use: Type !emo followed by the number (e.g., !emo 1)")
    
    return messages

# Initialize on import
initialize_numbered_emotes()
