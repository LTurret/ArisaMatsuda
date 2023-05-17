import json, os

import interactions

from core.secrets import tokens

Arisa = interactions.Client(
    token = tokens()["bot"],
    intents = interactions.Intents.ALL,
    presence = interactions.ClientPresence(
        activities = [
            interactions.PresenceActivity(
                name = "偶像大師 百萬人演唱會！ 劇場時光",
                type = interactions.PresenceActivityType.GAME
            )
        ]
    ),
    disable_sync=False
)

@Arisa.event
async def on_ready():
    try:
        os.system("clear")
    except Exception as _:
        pass
    print(f"Up!10sion♪\nEverybody attention!!")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        print(f"Loading slash command extension: {filename}")
        Arisa.load(f"cogs.{filename[:-3]}")

print("Booting...")

Arisa.start()