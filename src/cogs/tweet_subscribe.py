import logging

from os import getenv
from typing import List, Optional

from aiohttp import ClientSession
from tinydb import Query, TinyDB

from discord import Embed
from discord.ext.tasks import loop
from discord.ext.commands import Bot, Cog

from module.fetch_tweet import fetch_tweet
from module.html_parser import html_parser
from module.tweets_segment import segment
from module.content_util import ContentUtil
from module.embed_util import EmbedUtil


class TweetSubscribe(Cog):
    def __init__(self, Arisa) -> None:
        self.Arisa: Bot = Arisa
        self.config: TinyDB = TinyDB(getenv("path_db"))
        self.channel: Optional[int] = None
        self.pattern: str = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"
        logging.info(f"↳ Extension {__name__} created.")

    def __del__(self) -> None:
        logging.info(f"↳ Extension {__name__} removed.")

    @Cog.listener()
    async def on_ready(self):
        self.channel = self.Arisa.get_channel(int(getenv("retweet_subscribe_channel")))
        self.retweet.start()

    @loop(seconds=20)
    async def retweet(self):
        logging.debug("Fetching subscription list.")
        url: str = getenv("cdn_url")
        headers: dict = self.config.search(Query().name == "headers")[0]["value"]
        current_snowflake: int = self.config.search(Query().name == "snowflake")[0]["value"]

        async with ClientSession(headers=headers, trust_env=True) as session:
            async with session.get(url) as response:
                queue: List[str] = html_parser(await response.text())
                queue.sort()

        queue = segment(queue, current_snowflake)

        # Update snowflake
        if len(queue):
            logging.info("New tweet found in subscription channel, start sending to Discord.")
            upper_snowflake: int = queue[-1]
            snowflake_data: dict = {"name": "snowflake", "value": max(current_snowflake, upper_snowflake)}
            self.config.update(snowflake_data, Query().name == "snowflake")
            logging.info(f"snowflake updated: {upper_snowflake}")

        for tweet_id in queue:
            api_callback: dict = await fetch_tweet(tweet_id)
            content_util: ContentUtil = ContentUtil()
            content: dict = {**(await content_util.get_contents(api_callback))}
            embeds: List[Embed] = EmbedUtil(content, tweet_id, "百萬轉推魔法", 0xD8A604).embed_queue

            logging.info(f"{__name__}: Video processed succesfully and sent to channel.")
            await self.channel.send(files=content["videos"], embeds=embeds, allowed_mentions=None, silent=True)


async def setup(Arisa):
    await Arisa.add_cog(TweetSubscribe(Arisa))