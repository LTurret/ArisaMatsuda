import tomllib
import logging

from asyncio import run
from typing import Any, Dict
from logging import Logger
from os import getenv, listdir, sep

from discord import Game, Intents, Status
from discord.ext import commands
from dotenv import load_dotenv
from tinydb import TinyDB

from mapping import Directory


intents: Intents = Intents.default()
intents.message_content = True
Arisa: commands.Bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
Arisa.remove_command("help")


@Arisa.event
async def on_ready():
    await Arisa.change_presence(status=Status.online, activity=Game("⌒(*＞ｖ＜)b⌒"))
    # Syncing coulde cause 429 ratelimit, disable it when debugging.
    await Arisa.tree.sync()
    logging.info("Up!10sion♪ Everybody attention!!")


async def main():
    if not Directory.HEADERS.value.is_file():
        raise FileNotFoundError(rf"{Directory.HEADERS.value} does not exist!")

    if not Directory.DATABASE.value.is_file():
        logging.info(rf"Initializing database. Creating database {Directory.DATABASE.value}")
        database: TinyDB = TinyDB(Directory.DATABASE.value)
        initial_config: list = [{"name": "headers", "value": {}}, {"name": "snowflake", "value": 0}]

        for data in initial_config:
            database.insert(data)

    else:
        logging.info(rf"Found database, Loading {Directory.DATABASE.value}")
        database: TinyDB = TinyDB(Directory.DATABASE.value)

    # if path_keywords.is_file():
    #     with open(path_keywords, "r") as keywords_fp:
    #         keywords: dict = json.load(keywords_fp)
    #         database.insert(keywords)

    async with Arisa:
        for filename in listdir(f"{Directory.ROOT.value}{sep}cogs"):
            if filename.endswith(".py"):
                logging.debug(rf"Loading file: cogs/{filename}")
                await Arisa.load_extension(rf"cogs.{filename[:-3]}")

        await Arisa.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    # Initailization
    load_dotenv()
    with open(Directory.CONFIG.value, "rb") as config:
        config: Dict[str, Any] = tomllib.load(config)
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
        level=manifest[config["debug_flag"]],
        format="%(levelname)-5s %(asctime)s %(message)s ",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.debug("🚧 Debug mode enabled. 🚧")
    run(main())
