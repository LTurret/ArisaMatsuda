import random

import interactions

from core.scopes import Scopes

class post(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction
        self.content = ""

    @interactions.extension_command(
        name = "post",
        description = "匿名發文（可使用超連結文字格式）",
        scope = Scopes()["All"],
        options = [
            interactions.Option(
                name = "content",
                description = "想要問的問題",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def post(self, ctx: interactions.CommandContext, content: str):
        send = interactions.Button(
            style = interactions.ButtonStyle.PRIMARY,
            label = "Yes, send this message.",
            custom_id = "send"
        )
        self.content = content
        await ctx.send(content=f"輸入預覽：`{self.content}`\n輸入完成，確定送出嗎？", ephemeral=True, components=send)

    @interactions.extension_component("send")
    async def repeat_content(self, ctx):
        await ctx.send(self.content)

def setup(ArisaInteraction):
    post(ArisaInteraction)
