import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class ping(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "ping",
        description = "回傳延遲時間",
        scope = production
    ) 
    async def ping(self, ctx: interactions.CommandContext):
        await ctx.send(content=f"pong!\n{round(self.ArisaInteraction.latency)} ms")
    
def setup(ArisaInteraction):
    ping(ArisaInteraction)