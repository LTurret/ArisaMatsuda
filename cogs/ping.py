import interactions

class ping(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "ping",
        description = "回傳延遲時間"
    ) 
    async def ping(self, ctx: interactions.CommandContext):
        await ctx.send(content=f"pong!\n{round(self.ArisaInteraction.latency)} ms")
    
def setup(ArisaInteraction):
    ping(ArisaInteraction)