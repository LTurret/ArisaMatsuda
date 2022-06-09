import asyncio

from discord.ext import commands

class richpresence(commands.Cog):
    def __init__(self, Arisa):
        self.Arisa = Arisa

    @commands.command()
    async def rpcstart(self, ctx):
        await ctx.message.delete()
        while True:
            await asyncio.sleep(1200)
            print("ㄤ奈我醒了")

def setup(Arisa):
    Arisa.add_cog(richpresence(Arisa))