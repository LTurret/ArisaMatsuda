import logging

from asyncio import run
from os import getenv, listdir, path, sep, system

from discord import Game, Intents, Status
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
    system("clear")
    logging.info(f"ENTER→PLEASURE")


async def main():
    async with Arisa:
        for filename in listdir(f"{root}{sep}cogs"):
            if filename.endswith(".py"):
                await Arisa.load_extension(f"cogs.{filename[:-3]}")

        await Arisa.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run(main())
