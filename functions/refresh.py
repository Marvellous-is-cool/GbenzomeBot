from highrise import BaseBot
from highrise.models import User
from functions.emote_catalog import fetch_emote_catalog, all_emotes_list, free_emotes_list, premium_emotes_list

async def report_catalog_status(self: BaseBot):
    """Report the current status of the emote catalog"""
    await self.highrise.chat(f"📊 Emote Catalog Status:")
    await self.highrise.chat(f"Total emotes: {len(all_emotes_list)}")
    await self.highrise.chat(f"Free emotes: {len(free_emotes_list)}")
    await self.highrise.chat(f"Premium emotes: {len(premium_emotes_list)}")

async def refresh(self: BaseBot, user: User, message: str) -> None:
    """Refresh the emote catalog from the Highrise API
    
    Usage:
    !refresh - Refresh the emote catalog
    !refresh status - Show the current emote catalog status without refreshing
    """
    
    # Check if this is just a status request
    parts = message.lower().split()
    if len(parts) > 1 and parts[1] == "status":
        await report_catalog_status(self)
        return
    
    # Check if user is authorized to refresh
    # Use safe attribute access for owner_id and vip_users
    owner_id = getattr(self, 'owner_id', None)
    vip_users = getattr(self, 'vip_users', [])
    is_vip = user.id == owner_id or user.username in vip_users
    
    if not is_vip:
        await self.highrise.chat("❌ Only VIPs and the owner can refresh the emote catalog.")
        return
    
    # Inform user that refresh is starting
    await self.highrise.chat("🔄 Refreshing emote catalog from Highrise API...")
    
    try:
        # Fetch the emote catalog
        success = await fetch_emote_catalog(self)
        
        if success:
            await self.highrise.chat("✅ Emote catalog has been refreshed successfully!")
            # Show the updated catalog status
            await report_catalog_status(self)
        else:
            await self.highrise.chat("❌ Failed to refresh emote catalog from API. Using cached data if available.")
    
    except Exception as e:
        await self.highrise.chat(f"❌ Error refreshing emote catalog: {str(e)}")
