import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class ouen(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name="shy",
        description="亞利沙害羞",
        scope=production
    ) 
    async def shy(self, ctx):
        await ctx.send(content="<:ArisaShy:957861166082822195>")
    
def setup(ArisaInteraction):
    ouen(ArisaInteraction)