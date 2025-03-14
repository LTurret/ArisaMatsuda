import logging

from asyncio import sleep
from os import getenv
from re import findall, search
from typing import Final, List

from discord import AllowedMentions, Embed
from discord.ext.commands import Bot, Cog
from requests import patch

from class_logger import initialization, deletion
from module.fetch_tweet import fetch_tweet
from module.embed_util import EmbedUtil
from module.content_util import ContentUtil


class TweetParser(Cog):
    @initialization
    def __init__(self, Arisa) -> None:
        self.Arisa: Bot = Arisa
        self.pattern: Final[str] = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"

    @deletion
    def __del__(self) -> None:
        pass

    @Cog.listener()
    async def on_message(self, message: str):
        if search(self.pattern, message.content):
            async with message.channel.typing():
                channel_id: str = message.channel.id
                message_id: str = message.id
                headers: dict = {
                    "accept": "*/*",
                    "authorization": f'Bot {getenv("BOT_TOKEN")}',
                    "content-type": "application/json",
                }

                # Remove original message embedding object
                await sleep(0.25)
                patch(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=headers, data='{"flags":4}')

                # Find keyword
                if search(self.pattern, message.content):
                    tweet_id: str = search(self.pattern, message.content).group(1)
                    api_callback: dict = await fetch_tweet(tweet_id)

                    # Try follow the standard procedure or just send vxtwitter
                    try:
                        content_util: ContentUtil = ContentUtil()
                        content: dict = {**(await content_util.get_contents(api_callback))}
                        original_link: str = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                        embeds: List[Embed] = EmbedUtil(content, tweet_id, footer_text="(*>△<)<", original_link=original_link).embed_queue

                    except Exception as exception:
                        logging.error(exception)
                        result: List[tuple] = findall(r"(https://)(twitter|x)(.com/.+/status/\d+)", message.content)[0]
                        query: str = f"{result[0]}vxtwitter{result[-1]}"
                        await message.channel.send(query, reference=message, silent=True)

                    # Send embed
                    logging.debug([content["videos"], embeds])
                    await message.channel.send(
                        files=content["videos"], embeds=embeds, reference=message, allowed_mentions=AllowedMentions(replied_user=False), silent=True
                    )
                    logging.info(f"{__name__}: Tweet succesfully and sent to channel.")

    @Cog.listener()
    async def on_raw_message_delete(self, payload):
        channel = await self.Arisa.fetch_channel(payload.channel_id)
        pattern: str = rf".+\/({payload.message_id})"

        async for message in channel.history(limit=20):
            if message.author == self.Arisa.user:
                logging.debug(message.embeds[0].fields)
                if findall(pattern, message.embeds[0].fields[-1].value):
                    await message.delete()


async def setup(Arisa):
    await Arisa.add_cog(TweetParser(Arisa))
