import aiohttp
import asyncio
import json
import os

import interactions

from cogs.src.mltdevent.fetch import GetNewest, FetchBorder
from cogs.src.mltdevent.make import makefile
from cogs.src.mltdevent.image import makeimg 

with open("./config/scope.json") as server_scopes:
    server_scopes = json.load(server_scopes)
    production = server_scopes["Production"]
    testing = server_scopes["Testing"]

class mltdevent(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "event",
        description = "活動榜線圖",
        scope = production,
        options = [
            interactions.Option(
                name = "border_type",
                description = "選擇榜線類型",
                type = interactions.OptionType.STRING,
                required = True,
                choices = [
                    interactions.Choice(name="pt榜", value="pt"),
                    interactions.Choice(name="高分榜", value="hs"),
                    interactions.Choice(name="廳榜", value="lp"),
                ]
            )
        ]
    ) 
    async def event(self, ctx: interactions.CommandContext, border_type: str):

        announcement = ""
        announced = False

        matchtype = lambda typecode: ([3, 4, 5, 11, 13, 16].count(typecode)) == 1
        border_exists = lambda file: True if (len(file) > 0) else False

        async with aiohttp.ClientSession() as session:

            event_data = await GetNewest(session)
            identify = event_data["id"]

            if matchtype(event_data["type"]):
                announcement = "擷取新資料！"
                border_data = await FetchBorder(identify, session)
            else:
                announced = True
                announcement = "此活動無榜線喔⌒(*＞ｖ＜)b⌒"

            if not announced:
                
                os.chdir("./cogs")
                if "dist" not in os.listdir():
                    os.mkdir("dist")
                    os.chdir("./dist")
                    os.mkdir("mltdevent")
                    os.chdir("./mltdevent")
                    os.mkdir("image")
                    os.mkdir("data")
                os.chdir("../../../")

                tasks = [asyncio.create_task(makefile(event_data, "information"))]

                if border_exists(border_data):
                    tasks.append(asyncio.create_task(makefile(border_data, "border")))

                await asyncio.gather(*tasks)

                tasks = []
                tasks.append(makeimg(border_type))
                await asyncio.gather(*tasks)

                image = interactions.File(f"./cogs/dist/mltdevent/image/{border_type}.png")
                await ctx.channel.send(files=image)

        await ctx.send(content=announcement, ephemeral=True)
    
def setup(ArisaInteraction):
    mltdevent(ArisaInteraction)