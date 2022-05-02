import random

import discord

from discord.ext import commands

dictionary = {
    "望月杏奈": ["ANNA", "ㄤ奈", "ㄤ娜", "ㄤ那", "杏奈", "望月杏奈"]
}

class Keywords:
    def stable_search(self, content:str, category:str):
        for keyword in dictionary[category]:
            result:bool = content.upper().count(keyword) # Why make this O(n)
            if result:
                break
        return result
    
    # def set_search(self, content:str, category:str):
    #     return content.count(dictionary[category])

class ImagePath:
    def __init__(self):
        __BASE = "./image"
        __FUNCTIONAL = __BASE + "/functional"
        self.__ANNA_SLEEP = __FUNCTIONAL + "/anna_sleep/"
        self.__ANNA_EMOTES = __FUNCTIONAL + "/anna_emotes/"
        self.__MIRAI_GM = __FUNCTIONAL + "/mirai_gm/"

    def folder(self, selector:int=None, filename:str=""):
        manifest = {
            0: self.__ANNA_SLEEP,
            1: self.__ANNA_EMOTES,
            2: self.__MIRAI_GM
        }
        return f"{manifest[selector]}{filename}"

class keyword(commands.Cog):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        self.IMGPATH = ImagePath()
        self.KEYWORD = Keywords()

    @commands.Cog.listener()
    async def on_message(self, message):

        def not_bot():
            return message.author != self.Arisa.user

        # [MLTD] Webhook report
        TriggerPassword = message.content.count("TriggerWebhookConverter")
        if TriggerPassword and message.author.display_name == "音無小鳥":
            await message.delete()
            await message.channel.send(message.content[24:])

        # [ㄤ奈] ㄤ奈可愛
        if self.KEYWORD.stable_search(message.content, "望月杏奈") and message.content.count("可愛") and not_bot():
            MemberRoles = message.author.roles
            if str(MemberRoles).count("THE IDOLM@STER"):
                if str(message.author) == "LTurret#3420":
                    await message.channel.send("你很噁心... <:AnnaShock:954375272390606908>")
                else:
                    await message.channel.send("謝謝... 製作人 <:Su04:882135559043170315>💜")

        # [ㄤ奈] 睡覺
        if self.KEYWORD.stable_search(message.content, "望月杏奈") and message.content.count("睡覺"):
            image_location = self.IMGPATH.folder(selector=0, filename="anna_sleep.jpg")
            image = discord.File(image_location)
            await message.channel.send(file=image)

        # [ㄤ奈] >:)
        if message.content.count(">:)") and not_bot():
            image_location = self.IMGPATH.folder(selector=1, filename="anna_yes.png")
            image = discord.File(image_location)
            await message.channel.send(file=image)

        # [ㄤ奈] >:(
        if message.content.count(">:(") or message.content.count("😠") and not_bot():
            image_location = self.IMGPATH.folder(selector=1, filename="anna_mad.png")
            image = discord.File(image_location)
            await message.channel.send(file=image)

        # [ㄤ奈] 晚ㄤ奈
        if message.content.count("晚ㄤ奈") and not_bot():
            reply = [
                "晚ㄤ",
                "晚ㄤ奈喔~",
                "<:Su24:901163597340762172>",
                "<:Su09:882142223376977950>",
                f"{message.author.mention} 晚ㄤ奈~",
            ]
            reply = random.choice(reply)
            await message.channel.send(reply)
            emoji = random.choice(["<:Su09:882142223376977950>", "<:Su24:901163597340762172>"])
            await message.add_reaction(emoji)

        # [ㄤ奈] 早ㄤ奈
        if message.content.count("早ㄤ奈") and not_bot():
            if random.choice(range(2)):
                reply = [
                    "早ㄤ~~",
                    "早安",
                    "早ㄤ奈！",
                    "早ㄤ奈",
                    f"{message.author.mention} 早ㄤ奈~"
                ]
                reply = random.choice(reply)
                await message.channel.send(reply)
            else:
                image_location = self.IMGPATH.folder(selector=2, filename="gm.png")
                image = discord.File(image_location)
                await message.channel.send(file=image)

def setup(Arisa):
    Arisa.add_cog(keyword(Arisa))