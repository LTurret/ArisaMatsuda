from interactions import slash_command
from interactions import Extension
from interactions import SlashContext


class ping(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @slash_command(name="ping", description="回傳延遲時間")
    async def ping(self, ctx: SlashContext):
        await ctx.send(content=f"pong!\n{round(self.Arisa.latency)} ms")


def setup(Arisa):
    ping(Arisa)
