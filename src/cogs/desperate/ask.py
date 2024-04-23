from os import getenv
from re import findall
from re import search

from openai import AsyncOpenAI
from interactions import client
from interactions import listen
from interactions import Extension
from interactions import Message
from interactions.api.events import MessageCreate


class ask(Extension):
    def __init__(self, Arisa):
        self.Arisa: client = Arisa
        self.regex: str = r"<@943078700042301490>(.+)"
        self.MESSAGE: Message | None = None
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: MessageCreate):
        if findall(self.regex, event.message.content):
            self.MESSAGE = await event.message.channel.send("回應處理中！")
            query: str = search(self.regex, event.message.content).group(1)
            client: any = AsyncOpenAI(api_key=getenv("GPT_TOKEN"), base_url="https://api.chatanywhere.tech/v1")
            stream: any = await client.chat.completions.create(
                model=["gpt-3.5-turbo", "gpt-4"][0],
                messages=[
                    {
                        "role": "system",
                        "content": "妳是一位充滿活力的少女叫做「松田亜利沙」，妳最喜歡的偶像叫做「望月杏奈」。並且妳目前隸屬於「765Production」從事偶像藝能活動。妳的任何回答皆只能出現「正體-臺灣」、「英文」以及「日文」回應，在大多時候只選擇以「正體-臺灣」回應即可，但在回應時請不要提及語言名稱。對於粗言、髒話零容忍！",
                    },
                    {"role": "user", "content": query},
                ],
                stream=True,
            )
            message: str = ""
            async for chunk in stream:
                message += chunk.choices[0].delta.content or ""
            await self.MESSAGE.edit(content=message)
            self.MESSAGE = None


def setup(Arisa):
    ask(Arisa)
