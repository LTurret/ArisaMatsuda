from interactions import Extension, slash_command, SlashContext

class emotes(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @slash_command(
        name="shy",
        description="亞利沙害羞"
    ) 
    async def shy(self, ctx: SlashContext):
        await ctx.send(content="<:ArisaShy:957861166082822195>")
    
def setup(Arisa):
    emotes(Arisa)
