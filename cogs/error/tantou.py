import interactions

class tantou(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name="push",
        description="新增擔當",
        scope=[339368837356978187, 943075990295416842],
        choices=[
            interactions.Choice(
                name="望月杏奈",
                value="anna"
            )
        ]
    ) 
    async def add_role(self, ctx):
        message = await ctx.send(content="⌒(  ＞ヮ＜)⌒＜ 応援ください！")
        self.MESSAGE_CACHE = message
    
def setup(ArisaInteraction):
    tantou(ArisaInteraction)