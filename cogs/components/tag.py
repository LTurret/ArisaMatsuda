import json

import interactions, discord

with open("./configuration/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class ImagePath:
    def __init__(self):
        __BASE = "./image"
        __FUNCTIONAL = __BASE + "/functional"
        self.__TAG = __FUNCTIONAL + "/tag/"

    def folder(self, selector:int=None, filename:str=""):
        manifest = {
            0: self.__TAG
        }
        return f"{manifest[selector]}{filename}"

class tag(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction
        self.IMGPATH = ImagePath()

    @interactions.extension_command(
        name="tag",
        description="f-string",
        scope=[production, testing]
    )
    async def tag(self, ctx):
        image_location = self.IMGPATH.folder(selector=0, filename="fstring.png")
        image = discord.File(image_location)
        channel = await ctx.get_channel()
        await channel.send(file=image)
    
def setup(ArisaInteraction):
    tag(ArisaInteraction)