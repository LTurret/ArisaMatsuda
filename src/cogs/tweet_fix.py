import logging

from asyncio import sleep
from os import getenv
from re import findall, search
from typing import Final, Optional

from discord import Embed
from discord.ext.commands import Bot, Cog
from requests import patch

from module.fetch_tweet import fetch_tweet
from module.embed_util import EmbedUtil
from module.content_util import ContentUtil


class TweetFix(Cog):
    def __init__(self, Arisa):
        self.Arisa: Bot = Arisa
        self.channel: Optional[int] = None
        self.pattern: Final[str] = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"
        logging.info(f" ↳ Extension {__name__} loaded")

    @Cog.listener()
    async def on_message(self, message: str):
        if search(self.pattern, message.content):
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
                tweet_id: str = search(self.pattern, message.content).group(1)
                api_callback: dict = await fetch_tweet(tweet_id)

                # Try follow the standard procedure or just send vxtwitter
                try:
                    embeds: Optional[list[Embed]] = None
                    content_util: ContentUtil = ContentUtil()
                    content: dict = {**(await content_util.get_contents(api_callback))}
                    embeds: EmbedUtil = EmbedUtil(content, tweet_id, "(*>△<)<").embed_queue
                    logging.debug(embeds)

                except Exception as exception:
                    logging.critical(exception)
                    result: list[tuple] = findall(r"(https://)(twitter|x)(.com/.+/status/\d+)", message.content)[0]
                    query: str = f"{result[0]}vxtwitter{result[-1]}"
                    await message.channel.send(query, reference=message, silent=True)

                # Send embed
                # credit - kenneth (https://discord.com/channels/789032594456576001/1141430904644964412)
                try:
                    if content["videos"] is not None:
                        await message.channel.send(files=content["videos"], embeds=embeds, reference=message, allowed_mentions=None, silent=True)
                    else:
                        await message.channel.send(embeds=embeds, reference=message, allowed_mentions=None, silent=True)
                except:
                    logging.info(f"{__name__}: Message parser failed.")
                    await message.channel.send(embeds=embeds, reference=message, allowed_mentions=None, silent=True)


async def setup(Arisa):
    await Arisa.add_cog(TweetFix(Arisa))
