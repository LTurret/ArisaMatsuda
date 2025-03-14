import json
import logging

from os import getenv
from pathlib import Path
from typing import Dict

from discord.ext.commands import command, Bot, Cog

from class_logger import initialization, deletion
from mapping import MappingUtil


class Fun(Cog):
    @initialization
    def __init__(self, Arisa: Bot):
        self.Arisa: Bot = Arisa

    @deletion
    def __del__(self) -> None:
        pass

    @Cog.listener()
    async def on_message(self, message: str):
        NotImplemented
        # with open(MappingUtil.Directory.KEYWORDS.value, "r") as keywords_file:
        #     keywords: Dict = json.load(keywords_file)

        #     if message.content in keywords:
        #         async with message.channel.typing():
        #             resource_file: Path = Path(keywords[message.content])
        #             asset = File(BytesIO(Path(keywords[message.content])), filename="attachment.mp4")
        #             await message.channel.send()


async def setup(Arisa):
    await Arisa.add_cog(Fun(Arisa))
