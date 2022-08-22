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
        name = "event",
        description = "活動榜線圖",
        scope = production,
        options = [
            interactions.Option(
                name = "border_type",
                description = "選擇榜線類型",
                type = interactions.OptionType.STRING,
                required = True,
                choices = [
                    interactions.Choice(name="pt榜", value="eventPoint"),
                    interactions.Choice(name="高分榜", value="highScore"),
                    interactions.Choice(name="廳榜", value="loungePoint"),
                ]
            )
        ]
    ) 
    async def shy(self, ctx: interactions.CommandContext, border_type: str):
        await ctx.send(content=border_type)
    
def setup(ArisaInteraction):
    ouen(ArisaInteraction)