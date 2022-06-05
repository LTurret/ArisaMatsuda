import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class toggle(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name="toggle",
        description="開關頻道的檢視模式",
        scope=production,
        options=[
            interactions.Option(
                type=interactions.OptionType.BOOLEAN,
                name="view",
                description="是否檢視該頻道",
                required=True
            )
        ]
    ) 
    async def toggle(self, ctx):
        await ctx.send(content="test")
    
def setup(ArisaInteraction):
    toggle(ArisaInteraction)