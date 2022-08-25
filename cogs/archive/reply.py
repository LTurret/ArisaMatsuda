import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class reply(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "reply",
        description = "讓亞利沙重複你的訊息",
        scope = production,
        options = [
            interactions.Option(
                name = "message",
                description = "重複的訊息",
                type = interactions.OptionType.STRING,
                required = True
            ),
            interactions.Option(
                name = "identify",
                description = "回復的訊息的ID",
                type = interactions.OptionType.STRING,
                required = False
            )
        ]
    ) 
    async def reply(self, ctx: interactions.CommandContext, message: str, identify: str="0"):
        if identify != "0":
            reply_message = await ctx.channel.fetch_message(int(identify))
            await reply_message.reply(message)
        else:
            await ctx.send(content=message)

def setup(ArisaInteraction):
    reply(ArisaInteraction)
