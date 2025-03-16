import json
import logging

from pathlib import Path
from random import choice
from typing import Dict, List

from discord import AllowedMentions, File, Message
from discord.ext.commands import Bot, Cog

from class_logger import initialization, deletion
from mapping import Directory, FileType, MappingUtil


class Fun(Cog):
    @initialization
    def __init__(self, Arisa: Bot):
        self.Arisa: Bot = Arisa
        self.manager: MappingUtil = MappingUtil()
        with open(Directory.KEYWORDS.value, "r") as keywords_file:
            self.keywords: Dict = json.load(keywords_file)

    @deletion
    def __del__(self) -> None:
        pass

    @Cog.listener()
    async def on_message(self, message: Message):
        if not self.manager.config["features"]["fun"]:
            return

        if any((keyword := kw) in message.content for kw in self.keywords):
            trigger: str = self.keywords[keyword]
            directory: Path = Path(Directory.RESOURCE.value) / FileType[trigger["type"]].value["dir"] / trigger["dir"]

            if directory.is_dir():
                files: List[Path] = list(directory.glob("*"))
                directory: Path = choice(files)
                filetype: str = directory.suffix.lstrip(".")
            else:
                filetype: str = FileType[trigger["type"]].value["ext"]

            async with message.channel.typing():
                with directory.open("rb") as file_binary:
                    file: File = File(file_binary, filename=f"attachment.{filetype}")

                    await message.channel.send(file=file, reference=message, allowed_mentions=AllowedMentions(replied_user=False), silent=True)

                    logging.info(f"{__name__}: Fun attachment succesfully sent to channel.")


async def setup(Arisa):
    await Arisa.add_cog(Fun(Arisa))
