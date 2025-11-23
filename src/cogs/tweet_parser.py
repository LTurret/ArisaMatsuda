import logging
from asyncio import sleep
from os import getenv
from re import findall, search
from typing import Final

from discord import AllowedMentions, Embed
from discord.ext.commands import Bot, Cog
from discord.message import Message
from requests import patch

from src.class_logger import deletion, initialization
from src.module.content_util import ContentUtil
from src.module.embed_util import EmbedUtil
from src.module.fetch_tweet import fetch_tweet


class TweetParser(Cog):
    @initialization
    def __init__(self, Arisa: Bot) -> None:
        self.Arisa: Bot = Arisa
        self.pattern: Final[str] = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"

    @deletion
    def __del__(self) -> None:
        pass

    @Cog.listener()
    async def on_message(self, message: Message):
        if search(self.pattern, message.content):
            async with message.channel.typing():
                channel_id: int = message.channel.id
                message_id: int = message.id
                headers: dict[str, str] = {
                    "accept": "*/*",
                    "authorization": f'Bot {getenv("BOT_TOKEN")}',
                    "content-type": "application/json",
                }

                # Remove original message embedding object
                await sleep(0.25)
                _ = patch(f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}", headers=headers, data='{"flags":4}')

                # Find keyword
                if search(self.pattern, message.content):
                    tweet_id: str = search(self.pattern, message.content).group(1)
                    api_callback: dict = await fetch_tweet(tweet_id)

                    # Try follow the standard procedure or just send vxtwitter
                    try:
                        content_util: ContentUtil = ContentUtil()
                        content: dict = {**(await content_util.get_contents(api_callback))}
                        original_link: str = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                        embeds: list[Embed] = EmbedUtil(content, tweet_id, footer_text="(*>△<)<", original_link=original_link).embed_queue

                    except Exception as exception:
                        logging.error(exception)
                        result: list[tuple] = findall(r"(https://)(twitter|x)(.com/.+/status/\d+)", message.content)[0]
                        query: str = f"{result[0]}vxtwitter{result[-1]}"
                        await message.channel.send(query, reference=message, silent=True)

                    # Send embed
                    logging.debug([content["videos"], embeds])
                    await message.channel.send(
                        files=content["videos"], embeds=embeds, reference=message, allowed_mentions=AllowedMentions(replied_user=False), silent=True
                    )
                    logging.info(f"{__name__}: Tweet succesfully and sent to channel.")

    @Cog.listener()
    async def on_raw_message_delete(self, message: Message):
        channel = await self.Arisa.fetch_channel(message.channel_id)
        pattern: str = rf".+\/({message.message_id})"

        async for message in channel.history(limit=20):
            if message.author.bot and message.embeds:
                logging.debug(message.embeds[0].fields)
                if message.embeds and findall(pattern, message.embeds[0].fields[-1].value):
                    await message.delete()


async def setup(Arisa):
    await Arisa.add_cog(TweetParser(Arisa))
