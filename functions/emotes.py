from highrise import BaseBot
from highrise.models import User
from functions.emote_catalog import list_emotes, search_emote, get_emote_info

async def emotes(self: BaseBot, user: User, message: str) -> None:
    """Display the emote catalog with optional category and pagination
    
    Usage:
    !emotes - Show all emotes (page 1)
    !emotes free - Show only free emotes
    !emotes premium - Show only premium emotes
    !emotes <page> - Show specific page of all emotes
    !emotes <category> <page> - Show specific page of category
    !emotes search <term> [page] - Search for emotes by name
    !emotes info <name> - Get detailed information about a specific emote
    """
    # Parse the message to check for specific emote category
    parts = message.lower().split()
    
    # Default values
    category = "all"
    page = 1
    
    # Check for search command
    if len(parts) > 1 and parts[1] == "search" and len(parts) > 2:
        # Check if the last part is a page number
        page = 1
        search_parts = parts[2:]
        
        if search_parts[-1].isdigit():
            page = int(search_parts[-1])
            search_parts = search_parts[:-1]
        
        search_term = " ".join(search_parts)
        await self.highrise.chat(f"🔍 Searching for emotes matching '{search_term}'...")
        try:
            search_results = await search_emote(self, search_term, page)
            for msg in search_results:
                await self.highrise.chat(msg)
        except Exception as e:
            await self.highrise.chat(f"❌ Error searching for emotes: {e}")
        return
    
    # Check for info command
    elif len(parts) > 1 and parts[1] == "info" and len(parts) > 2:
        emote_name = " ".join(parts[2:])
        await self.highrise.chat(f"ℹ️ Getting information for emote '{emote_name}'...")
        try:
            info_results = await get_emote_info(self, emote_name)
            for msg in info_results:
                await self.highrise.chat(msg)
        except Exception as e:
            await self.highrise.chat(f"❌ Error getting emote information: {e}")
        return
    
    # Check if a category is specified
    elif len(parts) > 1 and parts[1] in ["all", "free", "premium"]:
        category = parts[1]
        # Check if page number is also specified
        if len(parts) > 2 and parts[2].isdigit():
            page = int(parts[2])
    # Only page number specified
    elif len(parts) > 1 and parts[1].isdigit():
        page = int(parts[1])

    await self.highrise.chat(f"📋 Fetching {category} emotes (page {page})...")
    
    try:
        # Get the emote list using the catalog
        messages = await list_emotes(self, category, page)
        
        # Send each message
        for message in messages:
            await self.highrise.chat(message)
    except Exception as e:
        await self.highrise.chat(f"❌ Error fetching emote catalog: {e}")
        await self.highrise.chat("Try using !allemo as an alternative.")
