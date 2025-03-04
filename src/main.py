import tomllib
import logging

from asyncio import run
from typing import Dict
from logging import Logger
from os import getenv, listdir, sep

from tinydb import TinyDB

from discord import Game, Intents, Status
from discord.ext import commands
from dotenv import load_dotenv

from mapping import MappingUtil


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
    if not MappingUtil.Directory.HEADERS.value.is_file():
        raise FileNotFoundError(rf"{MappingUtil.Directory.HEADERS.value} does not exist!")

    if not MappingUtil.Directory.DATABASE.value.is_file():
        logging.info(rf"Initializing database. Creating database {MappingUtil.Directory.DATABASE.value}")
        database: TinyDB = TinyDB(MappingUtil.Directory.DATABASE.value)
        initial_config: list = [{"name": "headers", "value": {}}, {"name": "snowflake", "value": 0}]

        for data in initial_config:
            database.insert(data)

    else:
        logging.info(rf"Found database, Loading {MappingUtil.Directory.DATABASE.value}")
        database: TinyDB = TinyDB(MappingUtil.Directory.DATABASE.value)

    # if path_keywords.is_file():
    #     with open(path_keywords, "r") as keywords_fp:
    #         keywords: dict = json.load(keywords_fp)
    #         database.insert(keywords)

    async with Arisa:
        for filename in listdir(f"{MappingUtil.Directory.ROOT.value}{sep}cogs"):
            if filename.endswith(".py"):
                logging.debug(rf"Loading file: cogs/{filename}")
                await Arisa.load_extension(rf"cogs.{filename[:-3]}")

        await Arisa.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    # Initailization
    load_dotenv()
    with open(MappingUtil.Directory.CONFIG.value, "rb") as config:
        config = tomllib.load(config)
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
