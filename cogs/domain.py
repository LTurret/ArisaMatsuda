import json

import interactions

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]

class domain(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "domain",
        description = "開關頻道的檢視模式",
        scope = production
    )
    async def domain(self, ctx: interactions.ComponentContext):
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
        message = await ctx.send("使用以下選單選擇領域：", components=selection, ephemeral=True)

    @interactions.extension_component("button")
    async def callback(self, ctx: interactions.ComponentContext, options: list[str]):
        for option in options:
            if any(list(map(lambda role_id: role_id == int(option), ctx.member.roles))):
                await ctx.member.remove_role(role=int(option), guild_id=production)
                await ctx.send(content="已離開該領域", ephemeral=True)
            else:
                await ctx.member.add_role(role=int(option), guild_id=production)
                await ctx.send(content="已加入該領域", ephemeral=True)

def setup(ArisaInteraction):
    domain(ArisaInteraction)