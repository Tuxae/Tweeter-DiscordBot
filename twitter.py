# coding: utf8
import discord
import requests
import asyncio
import aiohttp
import bs4
from bs4 import BeautifulSoup
from my_constants import TOKEN, channel_rer

url = "https://twitter.com/RERB?lang=fr"

class Tweet():
    
    def __init__(self,permalink,text):
        self.permalink = permalink
        self.text = text

def emoji_converter(emoji):
    return {
        "Emoji: Croix" : lambda : ":x:",
        "Emoji: Coche blanche en gras" : lambda : ":white_check_mark:",
        "Emoji: Triangle pointant vers la droite" : lambda : ":arrow_right:",
        "Emoji: Panneau chantier " : lambda : ":construction:",
        "Emoji: Index pointant vers la droite" : lambda : ":point_right:",
        "Emoji: Clé" : lambda : ":wrench:"
    }.get(emoji,lambda: None)()

def tweet_converter(tweet):
    s = ""
    for e in tweet.contents:
        # Image
        if e.name == "img" and "Emoji" in e.attrs.get("class"):
            emoji = emoji_converter(e.attrs.get("aria-label"))
            if emoji:
                s += emoji
        # Add text
        if type(e) is bs4.element.NavigableString:
            s += e
        # Transform @mention as text
        if e.name == "a" and "twitter-atreply" in e.attrs.get("class"):
            s += e.text
        # Add #hashtag as text
        if e.name == "a" and "twitter-hashtag" in e.attrs.get("class"):
            s += e.text
        # Add link as text
        if e.name == "a" and "twitter-timeline-link" in e.attrs.get("class"):
            s += " " + e.attrs.get("href")
    return s

client = discord.Client()

@client.event  
async def on_ready():  
    old_tweets_url = []
    print('Bot ready :-)') 
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    html = await r.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    tweets_p = soup.findAll("p", class_="tweet-text")
                    tweets_div = soup.findAll("div", class_="tweet")
                    tweets_url = [div.attrs.get("data-permalink-path") 
                            for div in tweets_div]
                    tweets_text = list(map(tweet_converter,tweets_p))
                    tweets = [Tweet(permalink, text) 
                            for permalink, text in zip(tweets_url,tweets_text)]
                    # Reverse the list to send tweets in the chronological order
                    tweets.reverse()
                    # When launched, old_tweets_url is empty
                    # Add the tweets in memory first, no need to send them
                    # in Discord
                    if len(old_tweets_url) > 0 :
                        for tweet in tweets:
                            if not tweet.permalink in old_tweets_url:
                                await client.get_channel(channel_rer).send(tweet.text)
                    old_tweets_url = tweets_url.copy()
                await asyncio.sleep(20)

client.run(TOKEN)
