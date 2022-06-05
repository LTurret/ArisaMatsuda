import random, os

import discord
from discord.ext import commands

dictionary = {
    "anna": ["ANNA", "ㄤ奈", "ㄤ娜", "ㄤ那", "杏奈", "望月杏奈"]
}

class IntegrationTools:
    def __init__(self):
        
        # Root
        __BASE = "./image"

        # Function directory
        __FUNCTIONAL = __BASE + "/functional"

        # Sub-function directory
        self.__ANNA_EMOTES = __FUNCTIONAL + "/anna_emotes/"
        self.__ANNA_KNOWS = __FUNCTIONAL + "/anna_knows/"
        self.__ANNA_SLEEP = __FUNCTIONAL + "/anna_sleep/"
        self.__MIRAI_GM = __FUNCTIONAL + "/mirai_gm/"
        self.__TAG_FUNNY = __FUNCTIONAL + "/tag_funny/"
        self.__YURIKO_CUP = __FUNCTIONAL + "/yuriko_cup/"
        
    def locf(self, selector:str=None, filename:str="", file:bool=True): # Abbreviation of "Locate Folder"

        # Return a directory to specific file.
        # The "file" argument can change to return a directory but not with specific file.

        manifest = {
            "AE": self.__ANNA_EMOTES,
            "AK": self.__ANNA_KNOWS,
            "AS": self.__ANNA_SLEEP,
            "MG": self.__MIRAI_GM,
            "TF": self.__TAG_FUNNY,
            "YC": self.__YURIKO_CUP
        }

        directory = f"{manifest[selector]}"

        if file:
            return f"{directory}{filename}"
        else:
            return directory[:-1]

    def stbs(self, content:str, category:str): # Abbreviation of "Stable Search"
        for keyword in dictionary[category]:
            result:bool = content.upper().count(keyword) # Why make this O(n)
            if result:
                break
        return result

class keyword(commands.Cog):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        self.IntegrationTools = IntegrationTools()

    @commands.Cog.listener()
    async def on_message(self, message):

        def not_bot(force:bool=False):
            if force:
                return True
            else:
                return message.author != self.Arisa.user

        try:

            # [MLTD] Webhook report
            TriggerPassword = message.content.count("TriggerWebhookConverter")
            if TriggerPassword and message.author.display_name == "音無小鳥":
                await message.delete()
                await message.channel.send(message.content[24:])

            # [ㄤ奈] ㄤ奈可愛
            if self.IntegrationTools.stbs(message.content, "anna") and message.content.count("可愛") and not_bot():
                MemberRoles = message.author.roles
                if str(MemberRoles).count("THE IDOLM@STER"):
                    if str(message.author) == "LTurret#3420":
                        await message.channel.send("你很噁心... <:AnnaShock:954375272390606908>")
                    else:
                        await message.channel.send("謝謝... 製作人 <:Su04:882135559043170315>💜")

            # [ㄤ奈] 睡覺
            if self.IntegrationTools.stbs(message.content, "anna") and message.content.count("睡覺") and not_bot():
                image = discord.File(self.IntegrationTools.locf("AS", "anna_sleep.jpg"))
                await message.channel.send(file=image)

            # [ㄤ奈] 窩不知道
            if self.IntegrationTools.stbs(message.content, "anna") and message.content.count("知道嗎") and not_bot():
                response = random.choice(os.listdir(self.IntegrationTools.locf("AK", file=False)))
                print(response)
                image = discord.File(self.IntegrationTools.locf("AK", response))
                await message.channel.send(file=image)

            # [ㄤ奈] >:)
            if message.content.count(">:)") and not_bot():
                image = discord.File(self.IntegrationTools.locf("AE", "anna_yes.png"))
                await message.channel.send(file=image)

            # [ㄤ奈] >:(
            if message.content.count(">:(") or message.content.count("😠") and not_bot():
                image = discord.File(self.IntegrationTools.locf("AE", "anna_mad.png"))
                await message.channel.send(file=image)

            # [ㄤ奈] 偷色色
            if message.content.count("ㄤ奈偷色色") and not_bot():
                image = discord.File(self.IntegrationTools.locf("AE", "anna_disclose.png"))
                await message.channel.send(file=image)
                await message.channel.send(random.choice(["窩沒有...", "沒... 沒有...", "...", "騙人的吧"]))

            # [ㄤ奈] 晚ㄤ奈
            if message.content.count("晚ㄤ奈") and not_bot():
                reply = [
                    "晚ㄤ",
                    "晚ㄤ奈喔~",
                    "<:Su24:901163597340762172>",
                    "<:Su09:882142223376977950>",
                    f"{message.author.mention} 晚ㄤ奈~",
                ]
                await message.channel.send(random.choice(reply))
                await message.add_reaction(random.choice(["<:Su09:882142223376977950>", "<:Su24:901163597340762172>"]))

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
                    await message.channel.send(random.choice(reply))
                else:
                    image = discord.File(self.IntegrationTools.locf("MG", "gm.png"))
                    await message.channel.send(file=image)

            # [ㄤ奈] 好色喔ㄤ奈
            if message.content.count("好色喔ㄤ奈") and not_bot():
                await message.channel.send("<:AnnaShy:954375272277352589>")

            # [Other] 百合子汁
            if message.content.count("百合子汁") and not_bot():
                image = discord.File(self.IntegrationTools.locf("YC", "YurikoCup.png"))
                await message.channel.send(file=image)

            # [Other] 打上池
            if message.content.count("打上池") and not_bot():
                channel = message.guild.get_channel(474858135853596675)
                reply_message = await channel.fetch_message(885778763932139530)
                await reply_message.reply(f"不要抽打上池")
                image = discord.File(self.IntegrationTools.locf("TF", "pullup.png"))
                await message.channel.send(file=image)

            # [Other] fstring
            if message.content.count("fstring") and not_bot():
                image = discord.File(self.IntegrationTools.locf("TF", "fstring.png"))
                await message.channel.send(file=image)
            
        except Exception as exception:
            print(exception)

def setup(Arisa):
    Arisa.add_cog(keyword(Arisa))