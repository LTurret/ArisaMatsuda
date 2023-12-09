from json import load
from os import path
from os import getenv
from os import sep
from re import search

from interactions import listen
from interactions import Extension
from interactions import Embed
from interactions import IntervalTrigger
from interactions import Task

from aiohttp import ClientSession

from cogs.module.embed_generator import embed_generator
from cogs.module.fetch_tweet import fetch_tweet
from cogs.module.get_contents import get_contents
from cogs.module.html_parser import html_parser
from cogs.module.tweets_trim import trim


class retweet(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        self.regex: str = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"
        self.upper_snowflake: int = 0
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_startup(self):
        self.retweet.start()

    @Task.create(IntervalTrigger(seconds=60))
    async def retweet(self):
        url: str = "https://nitter.net/imasml_theater"
        script_dir: str = path.dirname(path.realpath(__file__))

        assert "headers" not in f"{script_dir}{sep}config", "Please check is your header.json exists in config folder."

        with open(f"{script_dir}{sep}config{sep}headers.json", "r") as headers:
            headers: dict = load(headers)

        async with ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                queue: list[str] = html_parser(await response.text())
                queue.reverse()

        queue = trim(queue, self.upper_snowflake)

        # expression: str = r"https:\/\/.+\/imasml_theater\/status\/(\d+)"
        for url in queue:
            # Parsing tweetId
            tweetId: str = search(rf"{self.regex}", url).group(1)
            api_callback: dict = await fetch_tweet(tweetId)
            content: dict = {**(await get_contents(api_callback))}

            # Data handling
            embeds: list[Embed] = []
            
            if content["images"]:
                for image in content["images"]:
                    # Embeds composer - Compose multiple picture in to one array
                    embeds.append(embed_generator(content, image, tweetId=tweetId, color=0xD8A804))

            else:
                embeds.append(embed_generator(content, tweetId=tweetId, color=0xD8A804))

            CHANNEL = self.Arisa.get_channel(getenv("retweet_subscribe_channel"))

            try:
                if content["videos"] is not None:
                    await CHANNEL.send(files=content["videos"], embeds=embeds, silent=True)
            except:
                await CHANNEL.send(embeds=embeds, silent=True)

            # Update upper snowflake
            self.upper_snowflake = max(self.upper_snowflake, int(tweetId))


def setup(Arisa):
    retweet(Arisa)
