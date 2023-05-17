from interactions import Extension, slash_command, SlashContext

class ping(Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @slash_command(
        name = "ping",
        description = "回傳延遲時間"
    ) 
    async def ping(self, ctx: SlashContext):
        await ctx.send(content=f"pong!\n{round(self.ArisaInteraction.latency)} ms")
    
def setup(ArisaInteraction):
    ping(ArisaInteraction)