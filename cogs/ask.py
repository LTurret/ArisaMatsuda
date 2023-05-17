import json
import random

import interactions
import openai

from core.scopes import Scopes

class ask(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "ask",
        description = "問亞利沙",
        scope = Scopes()["All"],
        options = [
            interactions.Option(
                name = "question",
                description = "想要問的問題",
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
    )
    async def shy(self, ctx: interactions.CommandContext, question: str):
        with open("./config/openai.json", "r") as token:
            token = json.load(token)["token"]
        openai.api_key = token
        completion = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo",
                messages = [
                        {
                            "role": "user",
                            "content": f"你現在是一個很活潑的16歲女孩，請用繁體中文回答以下問題：「{question}」"
                        }
                    ]
                )
        await ctx.send(content=completion.choices[0].message.content)
    
def setup(ArisaInteraction):
    ask(ArisaInteraction)
