import random
import json
import os

QUESTIONS_FILE = "questions_data.json"

# 500 non-explicit, general/personal/social/life questions
QUESTIONS = [# Would You Rather
    "Be rich and single forever or broke but in love?",
    "Go viral for a meme or for a dance challenge?",
    "Lose your phone for 24 hours or your charger for 48?",
    "Never eat suya again or never eat shawarma again?",
    "Spend a weekend offline or a weekend broke?",

    # Relationships & Cringe
    "Worst DM you’ve ever received?",
    "Can you date someone who doesn’t like plantain?",
    "Texting first — a bold move or desperate?",
    "“I miss you” or “I bought you food” — which hits harder?",
    "Is love sweeter when it’s coded?",

    # Nigerian Gen Z Culture
    "What’s one thing Nigerians exaggerate the most?",
    "Which Nigerian aunty question gives you PTSD?",
    "What would your village people use to find you?",
    "Na who no get wahala dey do soft life abi?",
    "What’s the most “Nigerian” thing about you?",

    # Random/Playful
    "What would your TED Talk be about if it had to be unserious?",
    "Can you sleep through an earthquake if NEPA brings light?",
    "If money grew on trees, what would Nigeria look like?",
    "What’s your toxic but cute habit?",
    "Is it ever that deep?",

    # More Banter & Just Vibes
    "What’s your most controversial food take?",
    "If 'lazy' was a sport, what event would you win?",
    "What’s the funniest lie you told as a kid?",
    "Do you dance better alone or when people are watching?",
    "What’s the pettiest reason you’ve blocked someone?",

    # Fun & Light Hot Takes
    "What’s one habit you’ll never change even if it’s bad?",
    "Can you fight for love or you’ll just move on?",
    "What makes you feel instantly rich (even when you're not)?",
    "Money or more sleep — which do you need more right now?",
    "What emoji describes your current mood best?",

    # Youth Life & Daily Struggles
    "What’s a broke person hack you swear by?",
    "Would you rather hustle 24/7 or sleep like a baby?",
    "What's the longest you've gone without mobile data?",
    "Which food tastes better at night than during the day?",
    "Do you prefer borrowing money or borrowing charger?",

    # Social Media & Trends
    "Which trend needs to disappear forever?",
    "Have you ever unfollowed someone for oversharing?",
    "What social media habit secretly annoys you?",
    "Do you reply DMs immediately or mentally?",
    "Instagram comments or WhatsApp status replies — which is louder?",

    # Food & Naija Vibes
    "Beans or no beans with your rice?",
    "Eba, Amala, or Semo — who’s winning the swallow war?",
    "Can you trust someone who doesn’t eat pepper?",
    "Which street food is the GOAT?",
    "What drink tastes better in a sachet than in a bottle?",

    # Culture & Random Banter
    "What’s your Yoruba name even if you’re not Yoruba?",
    "What's your best fake excuse when you're late?",
    "Which music lyric lives in your head rent-free?",
    "Is Gen Z the funniest or the most confused generation?",
    "What’s something you’ll always gatekeep?",

    # Entertainment & Opinions
    "What’s the last movie you watched just for the hype?",
    "Afrobeats or Amapiano — what’s hotter right now?",
    "Would you rather be funny or fine?",
    "Which celebrity gives you 'bestie' energy?",
    "Which TV character lives rent-free in your mind?",

    # Self & Chill
    "How do you define 'vibe' in your own words?",
    "What’s your ideal soft life in 3 words?",
    "Sleep, gist, or food — pick two!",
    "What’s one thing that instantly ruins your mood?",
    "Are you a morning person or a certified night crawler?",

    # Games & Dares
    "Truth or dare — which one gives you more anxiety?",
    "How long can you keep a straight face during a prank?",
    "Have you ever chickened out of a challenge last minute?",
    "What’s the weirdest bet you’ve ever lost?",
    "Spin the bottle or charades — what’s your game night pick?",

    # Local Life
    "Have you ever shouted 'Up NEPA' unironically?",
    "Keke or okada — which one scares you more?",
    "How do you react when you see police on the road?",
    "Have you ever argued with a conductor over N50?",
    "What's your dream escape from Nigeria moment?",

    # Light Existential
    "If vibes paid bills, would you be rich?",
    "If your life was a meme, which one would it be?",
    "What's your favorite way to procrastinate?",
    "What random skill would you like to master?",
    "What would you name your alter ego?"
]

# Data persistence for picked questions per VIP

def load_questions_data():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_questions_data(data):
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(data, f)

def start_session(username):
    data = load_questions_data()
    data[username] = {"picked": [], "active": True}
    save_questions_data(data)
    return True

def stop_session(username):
    data = load_questions_data()
    if username in data:
        data[username]["active"] = False
        save_questions_data(data)
        return True
    return False

def get_question(username, num=None, random_pick=False):
    data = load_questions_data()
    if username not in data or not data[username].get("active"):
        return None, "Session not started. Use !ques start."
    picked = set(data[username]["picked"])
    available = [i for i in range(len(QUESTIONS)) if i not in picked]
    if not available:
        stop_session(username)
        return None, "All questions have been picked. Session ended."
    if random_pick:
        idx = random.choice(available)
    elif num is not None:
        if num < 1 or num > len(QUESTIONS):
            return None, f"Question number must be between 1 and {len(QUESTIONS)}."
        idx = num - 1
        if idx in picked:
            return None, "This question has already been picked."
    else:
        return None, "Invalid usage."
    data[username]["picked"].append(idx)
    save_questions_data(data)
    return QUESTIONS[idx], None

def get_all_questions():
    return QUESTIONS

# For admin: reset all sessions (not exposed to users)
def reset_all_sessions():
    if os.path.exists(QUESTIONS_FILE):
        os.remove(QUESTIONS_FILE)
