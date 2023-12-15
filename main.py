from os import getenv
from os import listdir
from os import path
from os import system

from dotenv import load_dotenv
from tinydb import TinyDB
from tinydb import Query

from interactions import listen
from interactions import Activity
from interactions import Client
from interactions import Intents


load_dotenv()

arisa = Client(intents=Intents.ALL, activity=Activity(name="偶像大師 百萬人演唱會！ 劇場時光"))


@listen()
async def on_startup():
    system("clear")
    print(f"Up!10sion♪\nEverybody attention!!")


for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        print(f"Loading extension: {filename}")
        arisa.load_extension(f"cogs.{filename[:-3]}")

print("Starting...")

if not path.isfile("config.json"):
    print('Creating "config.json"...')

    with open("config.json", "w"):
        print("Config.json created!")

    initial_config: list = [{"name": "headers", "value": {}}, {"name": "snowflake", "value": 0}]

    config = TinyDB("config.json")

    for data in initial_config:
        config.insert(data)
else:
    config = TinyDB("config.json")

assert path.isfile("headers.json"), '"/ArisaMatsuda/headers.json" is not exist!'
with open("headers.json", "r") as headers:
    import json

    headers = json.load(headers)
    headers_update: dict = {"name": "headers", "value": headers}
    config.update(headers_update, Query().name == "headers")

arisa.start(getenv("BOT_TOKEN"))
