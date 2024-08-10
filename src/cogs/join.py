import logging

from time import time

from discord import app_commands, Interaction, Object, SelectOption
from discord.ext.commands import Bot, Cog
from discord.ui import Select, View


class Join(Cog):
    def __init__(self, Arisa: Bot) -> None:
        self.Arisa: Bot = Arisa
        logging.info(f" ↳ Extension {__name__} loaded")

    @app_commands.command(name="join", description="開關頻道的檢視模式")
    async def join(self, interaction: Interaction) -> None:
        selection = Select(
            placeholder="選擇討論區（多選）",
            options=[
                SelectOption(label="Arts", value="1023609569529823273", description="藝術類別討論串", emoji="🔖"),
                SelectOption(label="Computer Science", value="712240674337980486", description="電腦科學類別討論串", emoji="🔖"),
                SelectOption(label="IM@S", value="672685805525008414", description="五家事務所偶像大師文字頻道", emoji="🔖"),
                SelectOption(label="IDOLY PRIDE", value="1075816300514902138", description="偶像榮耀文字頻道", emoji="💬"),
                SelectOption(label="Gaming", value="1090959289293742100", description="綜合遊戲頻道", emoji="💬"),
                SelectOption(label="Photos", value="1090959411633209374", description="綜合圖串", emoji="💬"),
                SelectOption(label="Nsfw", value="983712854156935229", description="色色頻道 - nsfw文字頻道", emoji="💬"),
                SelectOption(label="Meme", value="1081248335710654524", description="促咪齁搜災 - meme文字頻道", emoji="💬"),
            ],
            min_values=1,
            max_values=8,
        )

        async def join_callback(interaction):
            for value in interaction.values:
                if any(list(map(lambda role_id: role_id == int(value), interaction.member.roles))):
                    await interaction.member.remove_role(role=int(value))
                    await interaction.send(content="已離開該討論區", ephemeral=True)
                else:
                    await interaction.member.add_role(role=int(value))
                    await interaction.send(content="已加入該討論區", ephemeral=True)

        selection.callback = join_callback
        view = View()
        view.add_item(selection)
        message: str = f"""### <t:{int(time())}> </join:1112285216447401984>\n- 使用選單選擇加入討論區\n- 也可以使用 `j/<討論區>` 來快速加入/退出"""
        await interaction.response.send_message(message, view=view, ephemeral=True, silent=True, delete_after=30)


async def setup(Arisa):
    await Arisa.add_cog(Join(Arisa), guilds=[Object(id=339368837356978187)])
