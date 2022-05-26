from discord.ext import commands

class general(commands.Cog):
    def __init__(self, Arisa):
        self.Arisa = Arisa

    @commands.command()
    async def botsaid(self, ctx, *,message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def reply(self, ctx, reply_id, *,message):
        await ctx.message.delete()
        reply_message = await ctx.channel.fetch_message(reply_id)
        await reply_message.reply(message)
    
def setup(Arisa):
    Arisa.add_cog(general(Arisa))