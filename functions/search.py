from highrise import BaseBot
from highrise.models import User
from functions.emote_catalog import search_emote

async def search(self: BaseBot, user: User, message: str) -> None:
    """Search for emotes by name"""
    
    # Extract search term from message
    parts = message.split(" ", 1)
    if len(parts) < 2:
        await self.highrise.chat("Usage: !search <emote name>")
        return
    
    search_term = parts[1].strip()
    
    # Log the search attempt
    print(f"User {user.username} is searching for emote: {search_term}")
    
    # Perform the search
    await self.highrise.chat(f"🔍 Searching for emotes matching '{search_term}'...")
    
    try:
        # Get search results
        messages = await search_emote(self, search_term)
        
        # Send results
        for message in messages:
            await self.highrise.chat(message)
    
    except Exception as e:
        await self.highrise.chat(f"❌ Error while searching: {str(e)}")
