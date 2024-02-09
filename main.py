from os import getenv
from os import getcwd
from os import listdir
from os import sep
from os import system
from os.path import exists

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

root: str = f"{getcwd()}"
path_db: str = f"{root}{sep}database.json"
path_headers: str = f"{root}{sep}headers.json"

if not exists(path_db):
    print('Creating "database.json"...')

    with open(path_db, "w"):
        print(f'"{path_db}" created!')

    initial_config: list = [{"name": "headers", "value": {}}, {"name": "snowflake", "value": 0}]

    database = TinyDB(path_db)

    for data in initial_config:
        database.insert(data)
else:
    database = TinyDB(path_db)

assert exists(path_headers), f'"{path_headers}" is not exist!'
with open(path_headers, "r") as headers:
    import json

    headers = json.load(headers)
    headers_update: dict = {"name": "headers", "value": headers}
    database.update(headers_update, Query().name == "headers")

arisa.start(getenv("BOT_TOKEN"))
