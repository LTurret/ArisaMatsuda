import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class toggle(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    CATEGORIES = [
        interactions.Choice(name="偶像大師", value="672685805525008414"),
        interactions.Choice(name="藝術", value="1023609569529823273"),
        interactions.Choice(name="資訊工程", value="712240674337980486")
    ]

    @interactions.extension_command(
        name = "toggle",
        description = "開關頻道的檢視模式",
        scope = [production, testing],
        options = [
            interactions.Option(
                type = interactions.OptionType.STRING,
                name = "category",
                description = "開關領域討論區",
                required = False,
                choices = CATEGORIES
            )
        ]
    ) 
    async def toggle(self, ctx: interactions.CommandContext, category: str):
        print(ctx.member.roles)
        print(any(list(map(lambda role_id: role_id == int(category), ctx.member.roles))))
        if any(list(map(lambda role_id: role_id == int(category), ctx.member.roles))):
            await ctx.member.remove_role(role=int(category), guild_id=production)
            await ctx.send(content="已離開該領域", ephemeral=True)
        else:
            await ctx.member.add_role(role=int(category), guild_id=production)
            await ctx.send(content="已加入該領域", ephemeral=True)
    
def setup(ArisaInteraction):
    toggle(ArisaInteraction)