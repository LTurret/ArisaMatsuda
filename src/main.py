from asyncio import run
from os import getenv
from os import listdir
from os import path
from os import sep

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


intents: Intents = Intents.default()
intents.message_content = True
Arisa: commands.Bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
Arisa.remove_command("help")

root: str = path.dirname(path.realpath(__file__))


async def main():
    async with Arisa:
        for filename in listdir(f"{root}{sep}cogs"):
            if filename.endswith(".py"):
                await Arisa.load_extension(f"cogs.{filename[:-3]}")

        await Arisa.start(getenv("BOT_TOKEN", "None"))


if __name__ == "__main__":
    run(main())
