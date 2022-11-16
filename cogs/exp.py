import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class exp(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction
        self.MESSAGE_CACHE = [None, None]

    @interactions.extension_command(
        name = "exp",
        description = "experimental",
        scope = [production, testing]
    )
    async def exp(self, ctx: interactions.ComponentContext):
        selection = interactions.SelectMenu(
            options = [
                interactions.SelectOption(
                    label = "Arts",
                    emoji = interactions.Emoji(name="🎨"),
                    value = "1023609569529823273"
                ),
                interactions.SelectOption(
                    label = "CSIE",
                    emoji = interactions.Emoji(name="💻"),
                    value = "712240674337980486"
                )
            ],
            placeholder = "選擇領域（多選）",
            custom_id = "button",
            min_values = 1,
            max_values = 2
        )
        ouen_button = interactions.Button(
            style = interactions.ButtonStyle.PRIMARY,
            label = "關閉選單",
            custom_id = "close_button"
        )
        message = await ctx.send("Select your option:", components=selection)
        self.MESSAGE_CACHE[0] = message
        close = await ctx.send("手動關閉選單請按這裡", components=ouen_button, ephemeral=False)
        self.MESSAGE_CACHE[1] = close

    @interactions.extension_component("button")
    async def callback(self, ctx: interactions.ComponentContext, options: list[str]):
        for option in options:
            if any(list(map(lambda role_id: role_id == int(option), ctx.member.roles))):
                await ctx.member.remove_role(role=int(option), guild_id=production)
                await ctx.send(content="已離開該領域", ephemeral=True)
            else:
                await ctx.member.add_role(role=int(option), guild_id=production)
                await ctx.send(content="已加入該領域", ephemeral=True)

    @interactions.extension_component("close_button")
    async def ouen_response(self):
        await self.MESSAGE_CACHE[0].delete()
        await self.MESSAGE_CACHE[1].edit("已關閉選單", components=None, delete_after=2)

def setup(ArisaInteraction):
    exp(ArisaInteraction)