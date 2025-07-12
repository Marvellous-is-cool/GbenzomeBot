from highrise import *
from highrise.models import *
from highrise.webapi import *
from highrise.models_webapi import *
from functions.emote_catalog import list_emotes, fetch_emote_catalog

# Original emoteshelp list remains as a fallback
emoteshelp = ['kawai', 'hyped', 'emoji-halo', 'hero', 'astronaut', 'zombierun', 'dab', 'snake', 'loop-sad', 'loop-happy', 'kissing', 'emoji-shush', 'idle_tough', 'fail3', 'shocked', 'theatrical-test', 'fireworks', 'electrified', 'headless', 'armcannon', 'tiktok4', 'tiktok7', 'tiktok13', 'hiphop', 'hopscotch', 'outfit2', 'pose12', 'fading', 'pose13', 'profile-breakscreen', 'surf', 'cartwheel', 'kissing-passionate', 'tiktok1', 'flirt', 'receive-disappointed', 'gooey', 'oops', 'thief', 'sheephop', 'runhop', 'tiktok15', 'receive-happy', 'tiktok6', 'confused2', 'pose4', 'dinner', 'wavey', 'pose2', 'shuffle', 'twitched', 'juggling', 'tiktok6', 'opera', 'tiktok3', 'kid', 'anime3', 'tiktok16', 'tiktok12', 'tiktok5', 'cold', 'pose11', 'handwalk', 'dramatic', 'outfit', 'sit-chair', 'space', 'mining-mine', 'mining-success', 'mining-fail', 'pull', 'idle', 'cast', 'pull-small', 'small', 'hipshake', 'fruity', 'cheerleader', 'tiktok14', 'looping', 'floating', 'wild', 'howl', 'howl', 'trampoline', 'launch', 'cutesalute', 'salute', 'tiktok11', 'employee', 'gift', 'touch', 'sit-relaxed', 'sleigh', 'attention', 'jinglebell', 'timejump', 'toilet', 'nervous', 'wild', 'iceskating', 'sit-open', 'celebrate', 'shrink', 'pose10', 'shy2', 'puppet', 'headblowup', 'creepycute', 'creepypuppet', 'anime', 'pinguin', 'guitar', 'boxer', 'celebrationstep', 'pose6', 'pose9', 'stargazer', 'wrong', 'uwu', 'fashionista', 'icecream', 'gravity', 'punkguitar', 'tiktok4', 'cutey', 'pose5', 'pose3', 'pose1', 'casual', 'pose8', 'pose7', 'fighter', 'tiktok10', 'tiktok7', 'weird', 'tiktok9', 'cute', 'superpose', 'frog', 'idle_singing', 'energyball', 'maniac', 'swordfight', 'teleporting', 'float', 'telekinesis', 'slap', 'frustrated', 'embarrassed', 'enthusiastic', 'confused', 'shoppingcart', 'rofl', 'roll', 'superrun', 'superpunch', 'kicking', 'apart', 'hug', 'secrethandshake', 'peekaboo', 'monster_fmail', 'zombie', 'ropepull', 'proposing', 'sumo', 'charging', 'ninjarun', 'elbowbump', 'angry', 'baseball', 'floorsleeping', 'floorsleeping2', 'hugyourself', 'sad', 'death2', 'levelup', 'posh', 'snowangel', 'hot', 'snowball', 'lookup', 'curtsy', 'russian', 'bow', 'boo', 'fail1', 'fail2', 'jetpack', 'death', 'pennywise', 'sleep', 'idle_layingdown', 'theatrical', 'fainting', 'idle_layingdown2', 'wings', 'laughing2', 'tiktok2', 'model', 'blackpink', 'emoji-sick', 'idle_zombie', 'cold', 'bunnyhop', 'disco', 'sexy', 'heartfingers', 'tiktok8', 'ghost-idle', 'emoji-sneeze', 'emoji-pray', 'handstand', 'smoothwalk', 'singleladies', 'heartshape', 'emoji-ghost', 'aerobics', 'emoji-naughty', 'deathdrop', 'duckwalk', 'splitsdrop', 'voguehands', 'emoji-give-up', 'emoji-smirking', 'emoji-lying', 'emoji-arrogance', 'emoji-there', 'emoji-poop', 'emoji-hadoken', 'emoji-punch', 'handsup', 'metal', 'orangejustice', 'loop-aerobics', 'loop-annoyed', 'emoji-scared', 'think', 'loop-tired', 'headbobbing', 'disappear', 'emoji-crying', 'loop-tapdance', 'emoji-celebrate', 'emoji-eyeroll', 'emoji-dizzy', 'emoji-gagging', 'greedy', 'emoji-mind-blown', 'shy', 'emoji-clapping', 'hearteyes', 'suckthumb', 'exasperated', 'jumpb', 'exasperatedb', 'peace', 'wave', 'panic', 'harlemshake', 'tapdance', 'gangnam', 'no', 'sad', 'yes', 'kiss', 'gordonshuffle', 'nightfever', 'laughing', 'judochop', 'rainbow', 'robot', 'happy', 'emoji-angry', 'macarena', 'loop-sitfloor', 'emoji-thumbsup', 'tired', 'hello']


async def allemo(self: BaseBot, user: User, message: str) -> None:
    # Parse the message to check for specific emote category
    parts = message.lower().split()
    
    # Default values
    category = "all"
    page = 1
    
    # Check if a category is specified
    if len(parts) > 1 and parts[1] in ["all", "free", "premium"]:
        category = parts[1]
        # Check if page number is also specified
        if len(parts) > 2 and parts[2].isdigit():
            page = int(parts[2])
    # Only page number specified
    elif len(parts) > 1 and parts[1].isdigit():
        page = int(parts[1])

    await self.highrise.chat("Fetching emote list...")
    
    try:
        # Get the emote list using the catalog
        messages = await list_emotes(self, category, page)
        
        # Send each message
        for message in messages:
            await self.highrise.chat(message)
    except Exception as e:
        # Fallback to the original implementation
        await self.highrise.chat(f"Error fetching emote catalog: {e}")
        await self.highrise.chat("Using fallback emote list...")
        
        # Number of items to display per row
        items_per_row = 15
        chunks = [emoteshelp[i:i + items_per_row] for i in range(0, len(emoteshelp), items_per_row)]
        
        for chunk in chunks:
            await self.highrise.chat(", ".join(chunk))