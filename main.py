import os

import interactions

from core.secrets import tokens

arisa = interactions.Client(
    intents = interactions.Intents.ALL,
    activity = interactions.Activity(
        name = "偶像大師 百萬人演唱會！ 劇場時光"
    )
)

@interactions.listen()
async def on_startup():
    os.system("clear")
    print(f"Up!10sion♪\nEverybody attention!!")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        print(f"Loading extension: {filename}")
        arisa.load_extension(f"cogs.{filename[:-3]}")

print("Booting...")

arisa.start(token=tokens()["bot"])