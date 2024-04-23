import json

from os import path
from os import sep
from os import getenv
from re import findall
from re import search

import google.generativeai as genai

from google.generativeai.generative_models import GenerativeModel
from google.generativeai.types.generation_types import GenerateContentResponse
from google.generativeai.generative_models import ChatSession
from interactions import client
from interactions import listen
from interactions import Extension
from interactions import Message
from interactions.api.events import MessageCreate


class conversation(Extension):
    def __init__(self, Arisa):
        self.Arisa: client = Arisa
        self.regex: str = r"<@943078700042301490>(.+)"
        self.message: Message | None = None
        self.chat: ChatSession | None = None
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: MessageCreate):
        if findall(self.regex, event.message.content):
            self.message: Message = await event.message.channel.send("回應中", silent=True)

            root: str = rf"{path.dirname(path.realpath(__file__))}"
            resource: str = rf"{root}{sep}..{sep}..{sep}res"
            history_log: str = rf"{resource}{sep}history.json"

            # 對話初始化
            genai.configure(api_key=getenv("GEMINI_TOKEN"))
            model: GenerativeModel = GenerativeModel("gemini-pro")

            if not path.isfile(history_log):
                file: bytes = open(history_log, "w")
                file.write('{"history":[]}')
                file.close()
                print("對話記錄檔建立！")

            with open(history_log, "r") as file:
                conversation: list[dict] = json.load(file)
                self.chat: ChatSession = model.start_chat(history=conversation["history"])

            if not len(conversation["history"]):
                await self.message.edit(content="初始化中")
                self.chat = model.start_chat(history=[])
                response: GenerateContentResponse = self.chat.send_message(
                    "妳是一位充滿活力的少女叫做「松田亜利沙」，妳最喜歡的偶像叫做「望月杏奈」。並且妳目前隸屬於「765Production」從事偶像藝能活動。妳的任何回答皆只能出現「正體-臺灣」、「英文」以及「日文」回應，在大多時候只選擇以「正體-臺灣」回應即可，但在回應時請不要提及語言名稱。對於粗言、髒話零容忍！"
                )

            try:
                query: str = search(self.regex, event.message.content).group(1)
                response: GenerateContentResponse = self.chat.send_message(query)

                await self.message.edit(content=response.text)
                self.message = None
            except Exception as exception:
                print(exception)
                await self.message.edit(content="AI不給我回答這個 換個東西問問看")

            # 儲存聊天紀錄
            conversation: list[dict] = []
            for message in self.chat.history:
                context: str = findall(r"\"(.+)\"", str(message.parts))[0]
                context: str = context.replace("\\n", "")
                session: dict = {"role": message.role, "parts": [{"text": context}]}
                conversation.append(session)

            with open(history_log, "w") as file:
                json.dump({"history": conversation}, file, ensure_ascii=False, indent=2)


def setup(Arisa):
    conversation(Arisa)