import time

import interactions

from core.scopes import scopes

class join(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "join",
        description = "開關頻道的檢視模式",
        scope = scopes()["anna"]
    )
    async def join(self, ctx: interactions.ComponentContext):

        selection = interactions.SelectMenu(
            custom_id = "selections",
            options = [
                interactions.SelectOption(
                    label = "Arts",
                    value = "1023609569529823273",
                    description = "藝術類別討論串",
                    emoji = interactions.Emoji(name="🔖")
                ),
                interactions.SelectOption(
                    label = "Computer Science",
                    value = "712240674337980486",
                    description = "電腦科學類別討論串",
                    emoji = interactions.Emoji(name="🔖")
                ),
                interactions.SelectOption(
                    label = "IM@S",
                    value = "672685805525008414",
                    description = "五家事務所偶像大師文字頻道",
                    emoji = interactions.Emoji(name="🔖")
                ),
                interactions.SelectOption(
                    label = "IDOLY PRIDE",
                    value = "1075816300514902138",
                    description = "偶像榮耀文字頻道",
                    emoji = interactions.Emoji(name="💬")
                ),
                interactions.SelectOption(
                    label = "Gaming",
                    value = "1090959289293742100",
                    description = "綜合遊戲頻道",
                    emoji = interactions.Emoji(name="💬")
                ),
                interactions.SelectOption(
                    label = "Photos",
                    value = "1090959411633209374",
                    description = "綜合圖串",
                    emoji = interactions.Emoji(name="💬")
                ),
                interactions.SelectOption(
                    label = "Nsfw",
                    value = "983712854156935229",
                    description = "色色頻道 - nsfw文字頻道",
                    emoji = interactions.Emoji(name="💬")
                ),
                interactions.SelectOption(
                    label = "Meme",
                    value = "1081248335710654524",
                    description = "促咪齁搜災 - meme文字頻道",
                    emoji = interactions.Emoji(name="💬")
                )
            ],
            placeholder = "選擇討論區（多選）",
            min_values = 1,
            max_values = 8
        )
        message = f'''<t:{int(time.time())}> </join:1080308276186587236>\n使用選單選擇加入討論區：\n也可以使用 `j/<討論區>` 來快速加入/退出'''
        await ctx.send(message, components=selection, ephemeral=True)

    @interactions.extension_component("selections")
    async def callback(self, ctx: interactions.ComponentContext, options: list[str]):
        for option in options:
            if any(list(map(lambda role_id: role_id == int(option), ctx.member.roles))):
                await ctx.member.remove_role(role=int(option), guild_id=339368837356978187)
                await ctx.send(content="已離開該討論區", ephemeral=True)
            else:
                await ctx.member.add_role(role=int(option), guild_id=339368837356978187)
                await ctx.send(content="已加入該討論區", ephemeral=True)

def setup(ArisaInteraction):
    join(ArisaInteraction)
