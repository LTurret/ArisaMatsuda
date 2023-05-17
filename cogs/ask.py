import asyncio

from interactions import Extension, slash_command, slash_option, SlashContext, OptionType
import openai

from core.scopes import scopes
from core.secrets import tokens

async def chat(question: str):
    openai.api_key = tokens()["openai"]
    completion = await openai.ChatCompletion.acreate(
        model = "gpt-3.5-turbo",
        messages = [{
                "role": "user",
                "content": f"你現在是一位活潑的女孩子，叫做「松田亞利沙」，接下來的問題請以繁體中文回答：「{question}」"
            }])
    return completion

class ask(Extension):
    def __init__(self, bot):
        self.ArisaInteraction = bot
        self.CHANNEL_CACHE = None

    @slash_command(
        name = "ask",
        description = "問亞利沙",
        scopes = scopes()["all"]
    )
    @slash_option(
        name = "question",
        description = "想要問的問題",
        required = True,
        opt_type = OptionType.STRING
    )
    async def ask(self, ctx: SlashContext, question: str):
        self.CHANNEL_CACHE = ctx.channel
        message = await asyncio.gather(asyncio.create_task(chat(question)))
        content = message[0]["choices"][0]["message"]["content"]
        await self.CHANNEL_CACHE.send(content=content)

def setup(ArisaInteraction):
    ask(ArisaInteraction)
