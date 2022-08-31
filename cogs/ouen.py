import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class ouen(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction
        self.MESSAGE_CACHE = None

    @interactions.extension_command(
        name="ouen",
        description="為杏奈寶貝應援！！！！",
        scope=production
    ) 
    async def ouen(self, ctx):
        ouen_button = interactions.Button(
            style = interactions.ButtonStyle.PRIMARY,
            label = "\応援するよ！/",
            custom_id = "ouen_reply"
        )
        message = await ctx.send(content="⌒(  ＞ヮ＜)⌒＜ 応援ください！", components=ouen_button)
        self.MESSAGE_CACHE = message

    @interactions.extension_component("ouen_reply")
    async def ouen_response(self, ctx):
        await ctx.send("<:Anna:948915505064976485>", ephemeral=False)
        await self.MESSAGE_CACHE.edit("⌒(  ＞ヮ＜)⌒＜ 応援するよ！", components=None)
    
def setup(ArisaInteraction):
    ouen(ArisaInteraction)
