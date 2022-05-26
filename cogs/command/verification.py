import json

from discord.ext import commands

with open("./config/unique.json") as unique_ids:
    unique_ids = json.load(unique_ids)

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)

class const():
    def __init__(self):
        self.__GUILD:int = server_scopes["Production"]
        self.__CHANNEL_INFORMATION:int = unique_ids["CHANNEL_INFORMATION"]
        self.__MESSAGE:int = unique_ids["MESSAGE"]
        self.__ROLE:int = unique_ids["ROLE"]

    def id(self, selector:int):
        manifest = {
            0: self.__GUILD,
            1: self.__CHANNEL_INFORMATION,
            2: self.__MESSAGE,
            3: self.__ROLE
        }
        return manifest[selector]

class verification(commands.Cog):
    def __init__(self, Arisa):
        self.CONST = const()
        self.Arisa = Arisa

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == self.CONST.id(selector=1) and payload.message_id == self.CONST.id(selector=2):
            guild = self.Arisa.get_guild(self.CONST.id(selector=0))
            role = guild.get_role(self.CONST.id(selector=3))
            await payload.member.add_roles(role)

def setup(Arisa):
    Arisa.add_cog(verification(Arisa))