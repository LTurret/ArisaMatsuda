import tomllib
import logging

from asyncio import run
from typing import Any, Dict
from logging import Logger
from os import getenv, listdir
from pathlib import Path

from discord import Game, Intents, Status
from discord.ext import commands
from dotenv import load_dotenv

from mapping import Directory
from database import DatabaseUtil


intents: Intents = Intents.default()
intents.message_content = True
Arisa: commands.Bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
Arisa.remove_command("help")

with open(Directory.CONFIG.value, "rb") as CONFIG:
    CONFIG: Dict[str, Any] = tomllib.load(CONFIG)


@Arisa.event
async def on_ready():
    await Arisa.change_presence(status=Status.online, activity=Game("⌒(*＞ｖ＜)b⌒"))
    # Syncing coulde cause 429 ratelimit, disable it when debugging.
    await Arisa.tree.sync() if CONFIG["debug"]["sync"] else None
    logging.info("Up!10sion♪ Everybody attention!!")


async def main():
    assert Directory.HEADERS.value.is_file(), FileNotFoundError(rf"{Directory.HEADERS.value} not found!")
    DatabaseUtil.processing() if Directory.DATABASE.value.is_file() else DatabaseUtil.initialization()

    # if path_keywords.is_file():
    #     with open(path_keywords, "r") as keywords_fp:
    #         keywords: dict = json.load(keywords_fp)
    #         database.insert(keywords)

    async with Arisa:
        for filename in listdir(Path(Directory.ROOT.value / "cogs")):
            if filename.endswith(".py"):
                logging.debug(rf"Loading file: cogs/{filename}")
                await Arisa.load_extension(rf"cogs.{filename[:-3]}")

        await Arisa.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    # Initailization
    load_dotenv()
    manifest: Dict[str, str] = {False: logging.INFO, True: logging.DEBUG}

    # Logger Setup
    logger: Logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.CRITICAL)
    logging.basicConfig(
        filename="service.log",
        encoding="utf-8",
        filemode="a",
        level=manifest[CONFIG["debug"]["flag"]],
        format="%(levelname)-5s %(asctime)s %(message)s ",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.debug("🚧 Debug mode enabled. 🚧")

    try:
        run(main())
    except KeyboardInterrupt:
        logging.info("Shutting down...")
        Arisa.close()
        logging.info("Bye-bye!")
