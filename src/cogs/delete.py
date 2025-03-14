import logging

from discord.ext.commands import has_permissions, command, Bot, Cog

from class_logger import initialization, deletion


class Delete(Cog):
    @initialization
    def __init__(self, Arisa: Bot):
        self.Arisa: Bot = Arisa
        logging.debug(f"↳ Extension {__name__} loaded.")

    @deletion
    def __del__(self):
        pass

    @has_permissions(manage_messages=True)
    @command()
    async def cls(self, ctx, amount: int):
        await ctx.message.delete()
        if amount > 10:
            await ctx.send("訊息數量`>10`請分批執行。", ephemeral=True, silent=True)
        else:
            logging.info(f"{__name__}: {amount} messages purged.")
            await ctx.channel.purge(limit=amount)


async def setup(Arisa):
    await Arisa.add_cog(Delete(Arisa))
