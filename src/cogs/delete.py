from discord.ext import commands


class general(commands.Cog):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")
 

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def cls(self, ctx, amount: int):
        await ctx.message.delete()
        if amount > 10:
            await ctx.send("訊息數量`>10`請分批執行", ephemeral=True)
        else:
            await ctx.channel.purge(limit=amount)


async def setup(Arisa):
    await Arisa.add_cog(general(Arisa))