import json

import interactions

<<<<<<< HEAD:cogs/slash/ping.py
with open("./config/scope.json") as server_scopes:
=======
with open("./configuration/scope.json") as server_scopes:
>>>>>>> f074673c34e4b34f83d96f01e97434a5b1a9aaaf:cogs/components/ping.py
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
        await ctx.send(content=f"pong!\n{round(self.ArisaInteraction.latency)} ms")
    
def setup(ArisaInteraction):
    ping(ArisaInteraction)