import json

import interactions

with open("./configuration/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class ping(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction
        self.MESSAGE_CACHE = None

    @interactions.extension_command(
        name="ping",
        description="回傳延遲時間",
        scope=production
    ) 
    async def ping(self, ctx):
        await ctx.send(content=f"pong!\n{round(self.Arisa.latency*1000)} ms")
    
def setup(ArisaInteraction):
    ping(ArisaInteraction)