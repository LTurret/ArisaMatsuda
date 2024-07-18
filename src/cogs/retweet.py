import logging

from os import getenv, path, sep
from re import findall, search
from typing import Final, Optional

from aiohttp import sleep, ClientSession
from discord import Embed
from discord.ext.commands import has_permissions, command, Cog
from requests import patch
from tinydb import Query, TinyDB

from module.embed_util import embed_util
from module.fetch_tweet import fetch_tweet
from module.get_contents import get_contents
from module.html_parser import html_parser
from module.tweets_segment import segment


class twitter_fix(Cog):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        self.channel: Optional[int] = None
        self.pattern: Final[str] = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"
        # logging
        
    @Cog.listener()
    async def on_message(self, message: str):
        if search(self.pattern, message):
            channel_id: str = message.channel.id
            message_id: str = message.id
            headers: dict = {
                "accept": "*/*",
                "authorization": f'Bot {getenv("BOT_TOKEN")}',
                "content-type": "application/json",
            }

            await sleep(0.25)
            patch(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=headers, data='{"flags":4}')

            # Find keyword
            if search(self.pattern, message.content):
                tweet_id: str = search(self.pattern, message).group(1)
                api_callback: dict = await fetch_tweet(tweet_id)

                # Try follow the standard procedure or just send vxtwitter
                try:
                    embeds: Optional[list[Embed]] = None
                    content: dict = {**(await get_contents(api_callback))}
                    embed_queue: embed_util = embed_util(content, tweet_id, "(*>△<)<")

                    # if content["images"]:
                    #     for image in content["images"]:
                    #         # Embeds composer - Compose multiple picture in to one array
                    #         embeds.append(embed_generator(content, image, tweetId=tweet_id, footer_text="(*>△<)<"))
                    # else:
                    #     embeds.append(embed_generator(content, image, tweet_id=tweet_id, footer_text="(*>△<)<"))
                
                except Exception as exception:
                    logging.critical(exception)


async def setup(Arisa):
    await Arisa.add_cog(twitter_fix(Arisa))