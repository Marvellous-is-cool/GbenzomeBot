# bot.py

from highrise import BaseBot
from highrise.models import User
import asyncio, time, json, os, threading, yt_dlp, sounddevice as sd
import soundfile as sf

# 🗃️ Persistence
SONGS_FILE = 'song_data.json'

current_song = None
song_queue = []
song_history = []
song_start_time = 0
max_queue_per_user = 3
max_queue_length = 30

def save_song_data():
    with open(SONGS_FILE, 'w') as f:
        json.dump({'current_song': current_song,
                   'queue': song_queue, 'history': song_history}, f)

def load_song_data():
    global current_song, song_queue, song_history, song_start_time
    if os.path.exists(SONGS_FILE):
        with open(SONGS_FILE) as f:
            data = json.load(f)
        current_song = data.get('current_song')
        song_queue = data.get('queue', [])
        song_history = data.get('history', [])
        if current_song:
            song_start_time = time.time() - current_song.get('elapsed', 0)

load_song_data()

# 🎧 Helper: stream audio to virtual mic (BlackHole)
def play_file(path):
    data, fs = sf.read(path, dtype='float32')
    sd.default.device = 'BlackHole 2ch'
    sd.play(data, fs)
    sd.wait()

# Async wrapper
async def stream_and_wait(self, path):
    global current_song
    t = threading.Thread(target=play_file, args=(path,), daemon=True)
    t.start()
    # load duration via soundfile
    with sf.SoundFile(path) as f:
        duration = len(f) / f.samplerate
    await asyncio.sleep(duration)
    await self.highrise.chat(f"✅ Finished playing '{current_song['name']}'")
    current_song = None
    await process_song_queue(self)

# 🔄 Queue manager
def count_user(id):
    return sum(1 for s in song_queue if s['requester_id'] == id)

async def process_song_queue(self: BaseBot):
    global current_song, song_queue, song_history, song_start_time
    if current_song or not song_queue:
        if not song_queue:
            await self.highrise.chat("🎵 The queue is empty.")
        return

    next_song = song_queue.pop(0)
    current_song = next_song
    song_start_time = time.time()
    song_history.append(current_song)
    if len(song_history) > 50:
        song_history.pop(0)
    save_song_data()

    await self.highrise.chat(
        f"▶️ Now Playing: {current_song['name']} • Requested by {current_song['requester']}"
    )

    # Download and play
    def download():
        ydl_opts = {'format': 'bestaudio',
                    'outtmpl': 'cache/%(id)s.%(ext)s',
                    'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(current_song['name'], download=True)
            return ydl.prepare_filename(info)

    loop = asyncio.get_event_loop()
    path = await loop.run_in_executor(None, download)
    await stream_and_wait(self, path)

# 🗣️ Chat commands
# No need for SongBot class, we'll use individual functions that are called from main.py

async def request_song(self, user, message):
    global current_song, song_queue
    
    # Check if user is owner, VIP, or Host
    vip_users = getattr(self, 'vip_users', [])
    host_users = getattr(self, 'host_users', [])
    is_privileged = (user.id == self.owner_id or 
                    user.username.lower() in [vip.lower() for vip in vip_users] or
                    user.username.lower() in [host.lower() for host in host_users])
    
    if not is_privileged:
        return await self.highrise.chat("❌ Only owner, VIPs, and Hosts can request songs. Type !buyvip to become a VIP for 500g.")
    
    # Parse command: !req <song name> <artist>
    parts = message.split(" ", 2)
    if len(parts) < 3 or not parts[1].strip() or not parts[2].strip():
        return await self.highrise.chat("❌ Usage: !req <song name> <artist>")
    
    song_name = parts[1].strip()
    artist = parts[2].strip()
    search_query = f"{song_name} {artist}"
    
    if len(song_queue) >= max_queue_length:
        return await self.highrise.chat("❌ Queue is full.")
    if count_user(user.id) >= max_queue_per_user:
        return await self.highrise.chat("❌ Too many requests!")
    
    # Create entry with the search query (yt-dlp will search for it)
    entry = {
        "name": search_query, 
        "requester": user.username,
        "requester_id": user.id, 
        "requested_at": time.time(),
        "likes": 0, 
        "liked_by": []
    }
    
    song_queue.append(entry)
    save_song_data()
    await self.highrise.chat(f"✅ Added '{song_name}' by {artist} to queue at position #{len(song_queue)}")
    
    if not current_song:
        await process_song_queue(self)

async def skip_song(self, user):
    global current_song
    vip_users = getattr(self, 'vip_users', [])
    host_users = getattr(self, 'host_users', [])
    is_privileged = (user.id == self.owner_id or 
                    user.username.lower() in [vip.lower() for vip in vip_users] or
                    user.username.lower() in [host.lower() for host in host_users])
    
    if not is_privileged:
        return await self.highrise.chat("❌ Only owner, VIPs, and Hosts can skip.")
    if not current_song:
        return await self.highrise.chat("❌ No song playing.")
    await self.highrise.chat(f"⏭️ Skipped '{current_song['name']}'")
    current_song = None
    await process_song_queue(self)

async def like_song(self, user):
    global current_song
    if not current_song:
        return await self.highrise.chat("❌ Nothing playing.")
    if user.id in current_song['liked_by']:
        return await self.highrise.chat("❌ You already liked.")
    current_song['likes'] += 1
    current_song['liked_by'].append(user.id)
    save_song_data()
    await self.highrise.chat(f"❤️ {user.username} liked '{current_song['name']}' - {current_song['likes']} likes")

async def show_queue(self):
    global current_song, song_queue, song_start_time
    msgs = ["🎵 Queue:"]
    elapsed = int(time.time() - song_start_time) if current_song else 0
    if current_song:
        msgs.append(f"▶️ Now: {current_song['name']} • {format_time(elapsed)} • ❤️{current_song['likes']}")
    if song_queue:
        for i,s in enumerate(song_queue[:10],1):
            msgs.append(f"{i}. {s['name']} • by {s['requester']}")
        if len(song_queue)>10:
            msgs.append(f"...and {len(song_queue)-10} more")
    else:
        msgs.append("Empty. Request with !req <song> <artist> (VIPs and Hosts only)")
    for m in msgs:
        await self.highrise.chat(m)

async def now_playing(self):
    global current_song, song_start_time
    if not current_song:
        return await self.highrise.chat("🎵 No song playing.")
    elapsed = int(time.time()-song_start_time)
    await self.highrise.chat(f"▶️ Now: {current_song['name']} • {format_time(elapsed)} • ❤️{current_song['likes']}")

async def clear_queue(self, user):
    vip_users = getattr(self, 'vip_users', [])
    host_users = getattr(self, 'host_users', [])
    is_privileged = (user.id == self.owner_id or 
                    user.username.lower() in [vip.lower() for vip in vip_users] or
                    user.username.lower() in [host.lower() for host in host_users])
    
    if not is_privileged:
        return await self.highrise.chat("❌ Only owner, VIPs, and Hosts can clear.")
    removed = len(song_queue)
    song_queue.clear()
    save_song_data()
    await self.highrise.chat(f"🧹 Cleared {removed} songs")

def format_time(sec):
    m, s = divmod(sec, 60)
    return f"{m:02d}:{s:02d}"
