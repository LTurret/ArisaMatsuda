import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class help(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "help",
        description = "顯示說明",
        scope = production,
        options = [
            interactions.Option(
                name = "tag_name",
                description = "欲說明的選項",
                type = interactions.OptionType.STRING,
                required = True,
                choices = [
                    interactions.Choice(name="about_me", value="about_me"),
                    interactions.Choice(name="website", value="website"),
                    interactions.Choice(name="future", value="future"),
                    interactions.Choice(name="choices", value="choices")
                ]
            )
        ]
    )
    async def help(self, ctx: interactions.CommandContext, tag_name: str):

        manifest = {
            "about_me": "⌒(*＞ｖ＜)b⌒",
            "website": "歡迎來亞利沙公主，以後可能會有前後端服務：https://arisahi.me",
            "future": "亞利沙機器人以後不提供標記指令",
            "choices": "https://discord.com/channels/789032594456576001/790050201166675998/1011330607046991964"
        }

        await ctx.send(content=manifest[tag_name])
    
def setup(ArisaInteraction):
    help(ArisaInteraction)