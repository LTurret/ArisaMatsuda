import asyncio, json, os

import interactions, discord
from discord.ext import commands

with open("./config/token.json", mode="r") as token:
    token = json.load(token)

ArisaInteractions = interactions.Client(token=token["token"], intents=interactions.Intents.ALL, disable_sync=True)
Arisa = commands.Bot(command_prefix=commands.when_mentioned)
Arisa.remove_command('help')

@Arisa.event
async def on_ready():
    await Arisa.change_presence(status = discord.Status.online, activity = discord.Game("偶像大師 百萬人演唱會！ 劇場時光"))
    try:
        os.system("cls")
    except Exception as _:
        pass
    print(f"Up!10sion♪\nEverybody attention!!")

@Arisa.command()
async def load(ctx, extension):
    await ctx.message.delete()
    Arisa.load_extension(f"cogs.command.{extension}")
    await ctx.send(f"function **{extension}** loadeded.", delete_after = 5)

@Arisa.command()
async def unload(ctx, extension):
    await ctx.message.delete()
    Arisa.unload_extension(f"cogs.command.{extension}")
    await ctx.send(f"function **{extension}** unloaded.", delete_after = 5)

@Arisa.command()
async def reload(ctx, extension):
    await ctx.message.delete()
    Arisa.reload_extension(f"cogs.command.{extension}")
    await ctx.send(f"function **{extension}** reloaded.", delete_after = 5)

for filename in os.listdir("./cogs/slash"):
    if filename.endswith(".py"):
        print(f"Loading slash command extension: {filename}")
        ArisaInteractions.load(f"cogs.slash.{filename[:-3]}")

for filename in os.listdir("./cogs/command"):
    if filename.endswith(".py"):
        print(f"Loading commands extension: {filename}")
        Arisa.load_extension(f"cogs.command.{filename[:-3]}")

print("Booting...")

loop = asyncio.get_event_loop()

task1 = loop.create_task(ArisaInteractions._ready())
task2 = loop.create_task(Arisa.start(token["token"]))

gathered = asyncio.gather(task1, task2, loop=loop)
loop.run_until_complete(gathered)
