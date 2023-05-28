import time

import interactions
from interactions import Extension, slash_command, SlashContext, ChannelSelectMenu

from core.scopes import scopes

class join(Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @slash_command(
        name = "join",
        description = "開關頻道的檢視模式",
        scopes = [scopes()["anna"]]
    )
    async def join(self, ctx: interactions.ComponentContext):

        selection = interactions.StringSelectMenu(
            interactions.StringSelectOption(
                label = "Arts",
                value = "1023609569529823273",
                description = "藝術類別討論串",
                emoji = interactions.PartialEmoji(name="🔖")
            ),
            interactions.StringSelectOption(
                label = "Computer Science",
                value = "712240674337980486",
                description = "電腦科學類別討論串",
                emoji = interactions.PartialEmoji(name="🔖")
            ),
            interactions.StringSelectOption(
                label = "IM@S",
                value = "672685805525008414",
                description = "五家事務所偶像大師文字頻道",
                emoji = interactions.PartialEmoji(name="🔖")
            ),
            interactions.StringSelectOption(
                label = "Bi-general",
                value = "1112321667226681364",
                description = "跟配托利聊天的雙向頻道",
                emoji = interactions.PartialEmoji(name="💬")
            ),
            interactions.StringSelectOption(
                label = "IDOLY PRIDE",
                value = "1075816300514902138",
                description = "偶像榮耀文字頻道",
                emoji = interactions.PartialEmoji(name="💬")
            ),
            interactions.StringSelectOption(
                label = "Gaming",
                value = "1090959289293742100",
                description = "綜合遊戲頻道",
                emoji = interactions.PartialEmoji(name="💬")
            ),
            interactions.StringSelectOption(
                label = "Photos",
                value = "1090959411633209374",
                description = "綜合圖串",
                emoji = interactions.PartialEmoji(name="💬")
            ),
            interactions.StringSelectOption(
                label = "Nsfw",
                value = "983712854156935229",
                description = "色色頻道 - nsfw文字頻道",
                emoji = interactions.PartialEmoji(name="💬")
            ),
            interactions.StringSelectOption(
                label = "Meme",
                value = "1081248335710654524",
                description = "促咪齁搜災 - meme文字頻道",
                emoji = interactions.PartialEmoji(name="💬")
            ),
            custom_id = "selections",
            placeholder = "選擇討論區（多選）",
            min_values = 1,
            max_values = 9
        )
        message = f'''# <t:{int(time.time())}> </join:1112285216447401984>\n使用選單選擇加入討論區\n也可以使用 `j/<討論區>` 來快速加入/退出'''
        await ctx.send(message, components=selection, ephemeral=True)

    @interactions.component_callback("selections")
    async def callback(self, ctx: interactions.ComponentContext):
        for value in ctx.values:
            if any(list(map(lambda role_id: role_id == int(value), ctx.member.roles))):
                await ctx.member.remove_role(role=int(value))
                await ctx.send(content="已離開該討論區", ephemeral=True)
            else:
                await ctx.member.add_role(role=int(value))
                await ctx.send(content="已加入該討論區", ephemeral=True)

def setup(ArisaInteraction):
    join(ArisaInteraction)
