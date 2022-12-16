import interactions

from core.scopes import Scopes

class emotes(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name="shy",
        description="亞利沙害羞",
        scope=Scopes()["All"]
    ) 
    async def shy(self, ctx):
        await ctx.send(content="<:ArisaShy:957861166082822195>")
    
def setup(ArisaInteraction):
    emotes(ArisaInteraction)