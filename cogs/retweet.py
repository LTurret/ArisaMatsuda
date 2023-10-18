from json import dump
from json import load
from json import loads
from re import findall
from time import time
from os import getenv
from os import sep

from aiohttp import ClientSession
from bs4 import BeautifulSoup as bs

from interactions import listen
from interactions import Embed
from interactions import Extension
from interactions import IntervalTrigger
from interactions import Task

from cogs.src.embed_generator import embed_generator
from cogs.src.fetch_tweet import fetch_tweet
from cogs.src.get_contents import get_contents
from cogs.src.get_tokens import get_tokens


class retweet(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        self.max_ptr = None
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_startup(self):
        self.retweet.start()

    @Task.create(IntervalTrigger(seconds=120))
    async def retweet(self):
        cache_directory = f".{sep}cogs{sep}cache{sep}"
        with open(f"{cache_directory}{sep}latest_snowflake.json") as cache_file:
            self.max_ptr = load(cache_file)["latest"]

        user = "imasml_theater"
        cookies = {"auth_token": getenv("auth_token")}
        url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{user}"
        async with ClientSession(cookies=cookies) as session:
            async with session.get(url) as response:
                response = await response.text()

        html = bs(response, "html.parser")
        data = str(html.select("#__NEXT_DATA__")[0])
        data = findall(r">({.+)[<]", data)[0]
        data = loads(data)

        timeline = data["props"]["pageProps"]["timeline"]["entries"]
        timeline.reverse()
        queue = []
        for element in timeline:
            tweet = element["content"]["tweet"]
            if int(tweet["conversation_id_str"]) > self.max_ptr:
                self.max_ptr = int(tweet["conversation_id_str"])
                queue.append(tweet["conversation_id_str"])

        tokens: dict = {**(await get_tokens())}
        queue.reverse()
        while queue:
            tweetId = queue.pop()
            api_callback: dict = await fetch_tweet(tokens, tweetId)
            content: dict = {**(await get_contents(api_callback))}
            embeds: list = []

            # Embeds composer - used for multiple images
            if content["images"]:
                for image in content["images"]:
                    embeds.append(
                        embed_generator(
                            content,
                            image,
                            color=0xD8A804,
                            footer_icon="https://cdn.discordapp.com/attachments/714097668233625670/1164054918169104464/imas_theater_icon.png",
                        )
                    )
            else:
                init_embed: Embed = Embed(description=content["full_text"], color=0xD8A804, timestamp=time(), url="https://arisahi.me")
                init_embed.set_author(
                    name=f"{content['author']} (@{content['screen_name']})", url=f"https://twitter.com/{content['screen_name']}", icon_url=content["icon_url"]
                )
                init_embed.add_field(
                    name="原文傳送門",
                    value=f"[點我](https://twitter.com/{user}/status/{tweetId})",
                    inline=False,
                )
                init_embed.set_footer(
                    text="樓梯的轉推百萬魔法",
                    icon_url="https://cdn.discordapp.com/attachments/714097668233625670/1164054918169104464/imas_theater_icon.png",
                )
                embeds.append(init_embed)

            # Send embed
            CHANNEL = self.Arisa.get_channel(getenv("channel"))
            if content["video"] is not None:
                await CHANNEL.send(files=content["video"], embeds=embeds, silent=True)
            else:
                await CHANNEL.send(embeds=embeds, silent=True)

            with open(f"{cache_directory}{sep}latest_snowflake.json", "r") as cache_file:
                max_ptr = load(cache_file)
                max_ptr["latest"] = self.max_ptr

            with open(f"{cache_directory}{sep}latest_snowflake.json", "r+") as cache_file:
                dump(max_ptr, cache_file, indent=2)


def setup(Arisa):
    retweet(Arisa)
