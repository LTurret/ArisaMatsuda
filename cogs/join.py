import time

from os import getenv

from interactions import component_callback
from interactions import slash_command
from interactions import ComponentContext
from interactions import Extension
from interactions import StringSelectOption
from interactions import StringSelectMenu
from interactions import PartialEmoji


class join(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @slash_command(name="join", description="開關頻道的檢視模式", scopes=[getenv("production_server_anna")])
    async def join(self, ctx: ComponentContext):
        selection = StringSelectMenu(
            StringSelectOption(label="Arts", value="1023609569529823273", description="藝術類別討論串", emoji=PartialEmoji(name="🔖")),
            StringSelectOption(label="Computer Science", value="712240674337980486", description="電腦科學類別討論串", emoji=PartialEmoji(name="🔖")),
            StringSelectOption(label="IM@S", value="672685805525008414", description="五家事務所偶像大師文字頻道", emoji=PartialEmoji(name="🔖")),
            StringSelectOption(label="IDOLY PRIDE", value="1075816300514902138", description="偶像榮耀文字頻道", emoji=PartialEmoji(name="💬")),
            StringSelectOption(label="Gaming", value="1090959289293742100", description="綜合遊戲頻道", emoji=PartialEmoji(name="💬")),
            StringSelectOption(label="Photos", value="1090959411633209374", description="綜合圖串", emoji=PartialEmoji(name="💬")),
            StringSelectOption(label="Nsfw", value="983712854156935229", description="色色頻道 - nsfw文字頻道", emoji=PartialEmoji(name="💬")),
            StringSelectOption(label="Meme", value="1081248335710654524", description="促咪齁搜災 - meme文字頻道", emoji=PartialEmoji(name="💬")),
            custom_id="selections",
            placeholder="選擇討論區（多選）",
            min_values=1,
            max_values=8,
        )
        message = f"""### <t:{int(time.time())}> </join:1112285216447401984>\n- 使用選單選擇加入討論區\n- 也可以使用 `j/<討論區>` 來快速加入/退出"""
        await ctx.send(content=message, components=selection, ephemeral=True)

    @component_callback("selections")
    async def callback(self, ctx: ComponentContext):
        for value in ctx.values:
            if any(list(map(lambda role_id: role_id == int(value), ctx.member.roles))):
                await ctx.member.remove_role(role=int(value))
                await ctx.send(content="已離開該討論區", ephemeral=True)
            else:
                await ctx.member.add_role(role=int(value))
                await ctx.send(content="已加入該討論區", ephemeral=True)


def setup(Arisa):
    join(Arisa)
