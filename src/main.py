import json

from os import getenv
from os import listdir
from os import path
from os import sep
from os import system

from dotenv import load_dotenv
from tinydb import TinyDB
from tinydb import Query
from interactions import listen
from interactions import Activity
from interactions import Client
from interactions import Intents

Arisa = Client(delete_unused_application_cmds=True, intents=Intents.ALL, activity=Activity(name="偶像大師 百萬人演唱會！ 劇場時光"))


@listen()
async def on_startup():
    system("clear")
    print(f"Up!10sion♪\nEverybody attention!!")


print("Starting...")

root: str = path.dirname(path.realpath(__file__))
resource: str = f"{root}{sep}..{sep}res"
path_db: str = f"{resource}{sep}database.json"
path_headers: str = f"{resource}{sep}headers.json"

load_dotenv(f"{root}{sep}..{sep}.env")

if not path.isfile(path_db):
    print(f'Creating "{path_db}"...')
    database = TinyDB(path_db)
    initial_config: list = [{"name": "headers", "value": {}}, {"name": "snowflake", "value": 0}]

    for data in initial_config:
        database.insert(data)

else:
    database = TinyDB(path_db)

if not path.isfile(path_headers):
    raise FileNotFoundError(rf'"{path_headers}" is not exist!')

with open(path_headers, "r") as headers:
    headers = json.load(headers)
    headers_update: dict = {"name": "headers", "value": headers}
    database.update(headers_update, Query().name == "headers")

for filename in listdir(f"{root}{sep}cogs"):
    if filename.endswith(".py"):
        print(f"Loading extension: {filename}")
        Arisa.load_extension(f"cogs.{filename[:-3]}")

Arisa.start(getenv("BOT_TOKEN"))
