import logging

from asyncio import run
from os import environ, getenv, listdir, sep
from pathlib import Path

from tinydb import TinyDB

from discord import Game, Intents, Status
from discord.ext import commands
from dotenv import load_dotenv


intents: Intents = Intents.default()
intents.message_content = True
Arisa: commands.Bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
Arisa.remove_command("help")

# Define paths using Path
root: Path = Path(__file__).resolve().parent
cogs: Path = root / "cogs"
resource: Path = root.parent / "res"
path_db: Path = resource / "database.json"
path_headers: Path = resource / "headers.json"

# Convert Path objects to strings
environ["root"] = str(root)
environ["cogs"] = str(cogs)
environ["resource"] = str(resource)
environ["path_db"] = str(path_db)
environ["path_headers"] = str(path_headers)


@Arisa.event
async def on_ready():
    await Arisa.change_presence(status=Status.online, activity=Game("🚧 v2.0"))
    # Syncing coulde cause 429 ratelimit, disable it when debugging.
    # await Arisa.tree.sync(guild=Object(id=339368837356978187))
    logging.info("Up!10sion♪ Everybody attention!!")


async def main():
    # Initialize
    if not path_headers.is_file():
        raise FileNotFoundError(rf"{path_headers} does not exist!")

    if not path_db.is_file():
        logging.info(rf"Initializing database. Creating database {path_db}")
        database: TinyDB = TinyDB(path_db)
        initial_coinfig: list = [{"name": "headers", "value": {}}, {"name": "snowflake", "value": 0}]

        for data in initial_coinfig:
            database.insert(data)

    else:
        logging.info(rf"Found database, Loading {path_db}")
        database: TinyDB = TinyDB(path_db)

    async with Arisa:
        for filename in listdir(f"{root}{sep}cogs"):
            if filename.endswith(".py"):
                logging.debug(rf"Loading file: cogs/{filename}")
                await Arisa.load_extension(rf"cogs.{filename[:-3]}")

        await Arisa.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    load_dotenv()
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.CRITICAL)
    logging.basicConfig(
        filename="service.log",
        encoding="utf-8",
        filemode="a",
        level=logging.INFO,
        format="%(levelname)-5s %(asctime)s %(message)s ",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    run(main())
