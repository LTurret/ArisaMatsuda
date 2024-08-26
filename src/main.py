import logging

from asyncio import run
from os import getenv, listdir, path, sep, system

from discord import Game, Intents, Object, Status
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


intents: Intents = Intents.default()
intents.message_content = True
Arisa: commands.Bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
Arisa.remove_command("help")

root: str = path.dirname(path.realpath(__file__))


@Arisa.event
async def on_ready():
    await Arisa.change_presence(status=Status.online, activity=Game("🚧 v2.0"))
    await Arisa.tree.sync(guild=Object(id=339368837356978187))
    logging.info(f"ENTER→PLEASURE")


async def main():
    system("clear")
    async with Arisa:
        for filename in listdir(f"{root}{sep}cogs"):
            if filename.endswith(".py"):
                await Arisa.load_extension(f"cogs.{filename[:-3]}")

        await Arisa.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    logger = logging.getLogger("discord")
    logger.setLevel(logging.CRITICAL)
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.CRITICAL)
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(asctime)s %(message)s ", datefmt="%Y-%m-%d %H:%M:%S")
    run(main())
