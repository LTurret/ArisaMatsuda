import asyncio, json, os

import interactions

with open("./config/token.json", mode="r") as token:
    token = json.load(token)

Arisa = interactions.Client(
    token=token["token"],
    intents=interactions.Intents.ALL,
    presence=interactions.ClientPresence(
        activities=[
            interactions.PresenceActivity(
                name="偶像大師 百萬人演唱會！ 劇場時光",
                type=interactions.PresenceActivityType.GAME
            )
        ]
    ),
    disable_sync=False
)

@Arisa.event
async def on_ready():
    try:
        os.system("cls")
    except Exception as _:
        pass
    print(f"Up!10sion♪\nEverybody attention!!")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        print(f"Loading slash command extension: {filename}")
        Arisa.load(f"cogs.{filename[:-3]}")

print("Booting...")

loop = asyncio.get_event_loop()

task = loop.create_task(Arisa._ready())

gathered = asyncio.gather(task, loop=loop)
loop.run_until_complete(gathered)