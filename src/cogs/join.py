import logging

from time import time
from typing import List, Optional

from discord import app_commands, Role, Interaction, Object, SelectOption
from discord.ext.commands import Bot, Cog
from discord.ui import Select, View

from class_logger import initialization, deletion


class Join(Cog):
    @initialization
    def __init__(self, Arisa: Bot) -> None:
        self.Arisa: Bot = Arisa

    @deletion
    def __del__(self):
        pass

    @app_commands.command(name="join", description="開關頻道的檢視模式")
    async def join(self, interaction: Interaction) -> None:
        NotImplemented

    #     logging.info(f'{__name__}: called by "{interaction.user.name}".')
    #     selection = Select(
    #         placeholder="選擇討論區（多選）",
    #         options=[
    #             SelectOption(label="Arts", value="1023609569529823273", description="藝術類別討論串", emoji="🔖"),
    #             SelectOption(label="Computer Science", value="712240674337980486", description="電腦科學類別討論串", emoji="🔖"),
    #             SelectOption(label="IM@S", value="672685805525008414", description="五家事務所偶像大師文字頻道", emoji="🔖"),
    #             SelectOption(label="IDOLY PRIDE", value="1075816300514902138", description="偶像榮耀文字頻道", emoji="💬"),
    #             SelectOption(label="Gaming", value="1090959289293742100", description="綜合遊戲頻道", emoji="💬"),
    #             SelectOption(label="Photos", value="1090959411633209374", description="綜合圖串", emoji="💬"),
    #             SelectOption(label="Nsfw", value="983712854156935229", description="色色頻道 - nsfw文字頻道", emoji="💬"),
    #             SelectOption(label="Meme", value="1081248335710654524", description="促咪齁搜災 - meme文字頻道", emoji="💬"),
    #         ],
    #         min_values=1,
    #         max_values=8,
    #     )

    #     async def join_callback(interaction: Interaction):
    #         async with interaction.channel.typing():
    #             manifest_role_id: list[int] = [role.id for role in interaction.user.roles]

    #             for role in selection.values:
    #                 interaction_role: Optional[Role] = interaction.guild.get_role(int(role))
    #                 result: list[bool] = [role_id == int(role) for role_id in manifest_role_id]

    #                 if any(result):
    #                     await interaction.user.remove_roles(interaction_role)
    #                     await interaction.response.send_message(content="已離開該討論區", ephemeral=True, silent=True, delete_after=3)
    #                 else:
    #                     await interaction.user.add_roles(interaction_role)
    #                     await interaction.response.send_message(content="已加入該討論區", ephemeral=True, silent=True, delete_after=3)

    #     selection.callback = join_callback
    #     view = View()
    #     view.add_item(selection)
    #     message: str = f"""- 使用選單選擇加入討論區\n- 也可以使用 `j/<討論區>` 來快速加入/退出\n-# <t:{int(time())}> </join:1112308135235956736>\n"""
    #     await interaction.response.send_message(content=message, view=view, ephemeral=True, silent=True, delete_after=30)


async def setup(Arisa):
    await Arisa.add_cog(Join(Arisa), guilds=[Object(id=339368837356978187)])
