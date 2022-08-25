import json, random

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class ask(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "ask",
        description = "問亞利沙",
        scope = production,
        options = [
            interactions.Option(
                name = "question",
                description = "想要問的問題",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    ) 
    async def shy(self, ctx: interactions.CommandContext, question: str):
        choice = ["可以！", "<:ArisaShy:957861166082822195>", "亞利沙覺得不行..."]
        message = f"> {question}\n{random.choice(choice)}"
        await ctx.send(content=message)
    
def setup(ArisaInteraction):
    ask(ArisaInteraction)
