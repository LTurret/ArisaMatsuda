from os import getenv
from os import listdir
from os import system

from dotenv import load_dotenv

from interactions import listen
from interactions import Activity
from interactions import Client
from interactions import Intents

load_dotenv()

arisa = Client(
    intents = Intents.ALL,
    activity = Activity(
        name = "偶像大師 百萬人演唱會！ 劇場時光"
    )
)

@listen()
async def on_startup():
    system("clear")
    print(f"Up!10sion♪\nEverybody attention!!")

for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        print(f"Loading extension: {filename}")
        arisa.load_extension(f"cogs.{filename[:-3]}")

print("Starting...")

arisa.start(getenv("BOT_TOKEN"))