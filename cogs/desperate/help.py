from interactions import Extension, OptionType, SlashContext, SlashCommandChoice, slash_command, slash_option

from core.scopes import scopes

class help(Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @slash_command(
        name = "help",
        description = "顯示說明",
        scope = scopes()["all"]
    )
    @slash_option(
        name = "tag_name",
        description = "欲說明的選項",
        type = OptionType.STRING,
        required = True,
        choices = [
            SlashCommandChoice(name="about_me", value="about_me"),
            SlashCommandChoice(name="website", value="website"),
            SlashCommandChoice(name="future", value="future"),
            SlashCommandChoice(name="choices", value="choices"),
            SlashCommandChoice(name="button", value="button"),
        ])
    async def help(self, ctx: SlashContext, tag_name: str):

        if tag_name == "button":
            button_demo = interactions.Button(
                style = interactions.ButtonStyle.PRIMARY,
                label = "按鈕！",
                custom_id = "button_demo"
            )
            await ctx.send(content="按按看！", components=button_demo)
        else:
            manifest = {
                "about_me": "⌒(*＞ｖ＜)b⌒",
                "website": "歡迎來亞利沙公主，以後可能會有前後端服務：https://arisahi.me",
                "future": "亞利沙機器人以後不提供標記指令",
                "choices":
                "https://discord.com/channels/789032594456576001/790050201166675998/1011330607046991964",
            }
            await ctx.send(content=manifest[tag_name])

    @interactions.extension_component("button_demo")
    async def button_response(self, ctx):
        await ctx.send("按按鈕！", ephemeral=True)

def setup(ArisaInteraction):
    help(ArisaInteraction)