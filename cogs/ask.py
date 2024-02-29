from os import getenv
from re import findall
from re import search

import google.generativeai as genai

from dotenv import load_dotenv
from openai import AsyncOpenAI
from interactions import client
from interactions import listen
from interactions import modal_callback
from interactions import slash_command
from interactions import modal_callback
from interactions import ContextMenuContext
from interactions import Extension
from interactions import Modal
from interactions import ModalContext
from interactions import ParagraphText
from interactions.api.events import MessageCreate

load_dotenv()


class ask(Extension):
    def __init__(self, Arisa):
        self.Arisa: client = Arisa
        self.regex: str = r"<@943078700042301490>(.+)"
        print(f" ↳ Extension {__name__} created")

    @slash_command(name="ask", description="gpt-3.5-turbo 模型（Beta）")

    async def ping(self, ctx: ContextMenuContext):
        modal: Modal = Modal(
            ParagraphText(label="Long Input Text", custom_id="query"),
            title="提問問題",
            custom_id="ask",
        )
        await ctx.send_modal(modal=modal)

    @modal_callback("ask")
    async def on_modal_answer(self, ctx: ModalContext, query: str):
        await ctx.send(f"回應處理中！", ephemeral=True)
        client: any = AsyncOpenAI(api_key=getenv("GPT_TOKEN"), base_url="https://api.chatanywhere.tech/v1")
        stream: any = await client.chat.completions.create(
            model=["gpt-3.5-turbo", "gpt-4"][0],
            messages=[
                {"role": "system", "content": "妳是一位充滿活力的少女叫做「松田亜利沙」，妳最喜歡的偶像叫做「望月杏奈」。並且妳目前隸屬於「765Prodution」從事偶像藝能活動。妳的任何回答皆只能出現「正體-臺灣」、「英文」以及「日文」回應，在大多時候只選擇以「正體-臺灣」回應即可，但在回應時請不要提及語言名稱。對於粗言、髒話零容忍！"},
                {"role": "user", "content": query}],
            stream=True,
        )
        message: str = ""
        async for chunk in stream:
            message += chunk.choices[0].delta.content or ""
        await ctx.send(content=f"### ✨ {query}\n{message}")

    @listen()
    async def on_message_create(self, event: MessageCreate):
        if findall(self.regex, event.message.content):
            query: str = search(self.regex, event.message.content).group(1)
            token: str = getenv("GEMINI_TOKEN")
            genai.configure(api_key=token)
            model: genai = genai.GenerativeModel("gemini-pro")
            response: str = model.generate_content(query)
            await event.message.channel.send(response.text)


def setup(Arisa):
    ask(Arisa)
