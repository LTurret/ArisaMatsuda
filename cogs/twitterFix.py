from re import findall
from re import search

from interactions import events
from interactions import listen
from interactions import AllowedMentions
from interactions import Embed
from interactions import Extension

from cogs.modules.embed_generator import embed_generator
from cogs.modules.fetch_tweet import fetch_tweet
from cogs.modules.get_contents import get_contents


class twitterFix(Extension):
    def __init__(self, Arisa):
        self.Arisa: any = Arisa
        self.regex: str = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"

        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: events.MessageCreate):
        if event.message.author != self.Arisa.user:
            if search(rf"{self.regex}", event.message.content):
                await event.message.add_reaction("🎄")

    @listen()
    async def on_message_react(self, event: events.MessageReactionAdd):
        if event.reaction.count > 1 and event.reaction.me:
            # Clear reactions
            await event.reaction.remove()

            # Find keyword
            if search(rf"{self.regex}", event.message.content):
                tweetId: str = search(rf"{self.regex}", event.message.content).group(1)
                api_callback: dict = await fetch_tweet(tweetId)

                # Try follow the standard procedure or just send vxtwitter
                try:
                    content: dict = {**(await get_contents(api_callback))}
                    embeds: list[Embed] = []

                    if content["images"]:
                        for image in content["images"]:
                            # Embeds composer - Compose multiple picture in to one array
                            embeds.append(embed_generator(content, image, tweetId=tweetId))

                    else:
                        embeds.append(embed_generator(content, tweetId=tweetId))

                except Exception:
                    result: list[tuple] = findall(r"(https://)(twitter|x)(.com/.+/status/\d+)", event.message.content)[0]
                    message: str = f"{result[0]}vxtwitter{result[-1]}"
                    await event.message.channel.send(message, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True)

                # Send embed
                # credit - kenneth (https://discord.com/channels/789032594456576001/1141430904644964412)
                if content["videos"] is not None:
                    await event.message.channel.send(
                        files=content["videos"], embeds=embeds, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True
                    )
                else:
                    await event.message.channel.send(embeds=embeds, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True)


def setup(Arisa):
    twitterFix(Arisa)
