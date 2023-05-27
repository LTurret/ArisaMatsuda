from interactions import Extension, slash_command, SlashContext

class ping(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa

    @slash_command(
        name = "ping",
        description = "回傳延遲時間"
    ) 
    async def ping(self, ctx: SlashContext):
        await ctx.send(content=f"pong!\n{round(self.Arisa.latency)} ms")
    
def setup(Arisa):
    ping(Arisa)