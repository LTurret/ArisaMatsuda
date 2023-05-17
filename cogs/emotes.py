import interactions

from interactions import Extension, slash_command, SlashContext

class emotes(Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @slash_command(
        name="shy",
        description="亞利沙害羞"
    ) 
    async def shy(self, ctx: SlashContext):
        await ctx.send(content="<:ArisaShy:957861166082822195>")
    
def setup(ArisaInteraction):
    emotes(ArisaInteraction)
