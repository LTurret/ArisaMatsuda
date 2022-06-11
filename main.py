import json, os

import interactions, discord

with open("./config/token.json", mode="r") as token:
    token = json.load(token)

Arisa = interactions.Client(token=process.env.TOKEN, intents=interactions.Intents.ALL, disable_sync=True)

@Arisa.event
async def on_ready():
    await Arisa.change_presence(status = discord.Status.online, activity = discord.Game("偶像大師 百萬人演唱會！ 劇場時光"))
    try:
        os.system("cls")
    except Exception as _:
        pass
    print(f"Up!10sion♪\nEverybody attention!!")

for filename in os.listdir("./cogs/slash"):
    if filename.endswith(".py"):
        print(f"Loading slash command extension: {filename}")
        Arisa.load(f"cogs.slash.{filename[:-3]}")

print("Booting...")

Arisa._ready()
