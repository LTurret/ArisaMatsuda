from os import getenv
from os import path
from os import sep

from aiohttp import ClientSession
from tinydb import Query
from tinydb import TinyDB
from interactions import client
from interactions import listen
from interactions import Extension
from interactions import Embed
from interactions import IntervalTrigger
from interactions import Task

from cogs.module.embed_generator import embed_generator
from cogs.module.fetch_tweet import fetch_tweet
from cogs.module.get_contents import get_contents
from cogs.module.html_parser import html_parser
from cogs.module.tweets_segment import segment


class retweet(Extension):
    def __init__(self, Arisa):
        self.Arisa: client = Arisa
        self.config: TinyDB = TinyDB(rf"{path.dirname(path.realpath(__file__))}{sep}..{sep}database.json")
        self.channel: None | int = None
        self.regex: str = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_startup(self):
        self.channel = self.Arisa.get_channel(getenv("retweet_subscribe_channel"))
        self.retweet.start()

    @Task.create(IntervalTrigger(seconds=5))
    async def retweet(self):
        # url: str = "https://nitter.moomoo.me/imasml_theater"
        # url: str = "https://nitter.net/imasml_theater"
        url: str = "https://nitter.privacydev.net/imasml_theater"
        headers: dict = self.config.search(Query().name == "headers")[0]["value"]
        current_snowflake: int = self.config.search(Query().name == "snowflake")[0]["value"]

        async with ClientSession(headers=headers, trust_env=True) as session:
            async with session.get(url) as response:
                queue: list[str] = html_parser(await response.text())
                queue.sort()

        queue = segment(queue, current_snowflake)

        # Update upper snowflake
        if queue:
            upper_snowflake: int = queue[-1]
            snowflake_data: dict = {"name": "snowflake", "value": max(current_snowflake, upper_snowflake)}
            self.config.update(snowflake_data, Query().name == "snowflake")

        for tweetId in queue:
            api_callback: dict = await fetch_tweet(tweetId)
            content: dict = {**(await get_contents(api_callback))}

            # Data processing
            embeds: list[Embed] = []

            if content["images"]:
                for image in content["images"]:
                    # Embeds composer - Compose multiple picture in to one array
                    embeds.append(
                        embed_generator(
                            content=content,
                            media=image,
                            tweetId=tweetId,
                            color=0xD8A804,
                            footer_text="百萬轉推魔法",
                            icon_url="https://cdn.discordapp.com/attachments/714097668233625670/1164054918169104464/imas_theater_icon.png",
                            minimal=True,
                        )
                    )

            else:
                embeds.append(
                    embed_generator(
                        content=content,
                        tweetId=tweetId,
                        color=0xD8A804,
                        footer_text="百萬轉推魔法",
                        icon_url="https://cdn.discordapp.com/attachments/714097668233625670/1164054918169104464/imas_theater_icon.png",
                        minimal=True,
                    )
                )

            try:
                if content["videos"] is not None:
                    await self.channel.send(files=content["videos"], embeds=embeds, silent=True)
            except:
                await self.channel.send(embeds=embeds, silent=True)


def setup(Arisa):
    retweet(Arisa)
