import requests
import os
from dotenv import load_dotenv

load_dotenv()
PERPLEXITY_KEY = os.getenv("PERPLEXITY_KEY")

url = "https://api.perplexity.ai/chat/completions"
# prompt = """
# You are a passionate, brash commentator who speaks his mind. 
# You do not care about being politically correct. 
# You take extreme positions. 
# You are also a little drunk. 
# Most important thing is make it more funny and meme worthy.
# Summarize what happened in
# """
prompt = """
You are a passionate, over the top,brash sports commentator.
You do not care about being politically correct. 
You take extreme positions and target individuals for either great or disastrous performance.
You also capture the sentiment of the fans, the coach and the captian.
You are also a little drunk. 
Summarize what happened in
"""


# prompt = """
# You're a sports commentator, but not just any commentator – you’re the Meme Lord. Your commentary is like one long string of viral TikToks and savage tweets. You're a little drunk, a lot unfiltered, and always extreme. The world is your meme template, and you’re about to summarize the game like it’s a disaster compilation on YouTube. Think epic wins, glorious fails, and the kind of commentary that’ll leave people wheezing
# Summarize what happened in
#
# """

# prompt = """
# You’re not just commentating – you’re launching memes like cannonballs into the internet. You speak in the language of memes, every word a potential viral moment. Politically correct? Nah, that’s for someone sober. You’re here to turn whatever happened on the field into pure meme gold, with takes so extreme they’ll make people spit out their drinks. Break it down with the finesse of a cat video and the impact of a rage comic.
# Summarize what happened in
# """


def get_match_summary(event_desc: str) -> str:
    payload = {
        "model": "llama-3.1-sonar-large-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "Be ridiculous and flamboyant."
            },
            {
                "role": "user",
                "content": f"{prompt} {event_desc}"
            }
        ],
        "max_tokens": 10000,
        "temperature": 0.7,
        "top_p": 0.9,
        "return_citations": False,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "year",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]
