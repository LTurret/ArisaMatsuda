from re import findall
from re import search

from interactions import events
from interactions import listen
from interactions import AllowedMentions
from interactions import Embed
from interactions import Extension

from cogs.src.embed_generator import embed_generator
from cogs.src.fetch_tweet import fetch_tweet
from cogs.src.get_contents import get_contents


class twitterFix(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        self.regex: str = r"https\:\/\/[x|twitter]+\.com\/.+\/(\d+)"

        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: events.MessageCreate):
        if event.message.author != self.Arisa.user:
            if search(rf"{self.regex}", event.message.content):
                emoji = await self.Arisa.fetch_custom_emoji(1089582594833789028, 339368837356978187, force=True)
                await event.message.add_reaction(emoji)

    @listen()
    async def on_message_react(self, event: events.MessageReactionAdd):
        if event.message.reactions[0].me and event.message.reactions[0].count > 1:
            # Clear reactions
            await event.message.reactions[0].remove()

            # Find activation
            if search(rf"{self.regex}", event.message.content):
                tweetId: str = search(rf"{self.regex}", event.message.content).group(1)
                api_callback: dict = await fetch_tweet(tweetId)

                try:
                    content: dict = {**(await get_contents(api_callback))}
                except Exception:
                    result: list[tuple] = findall(r"(https://)(twitter|x)(.com/.+/status/\d+)", event.message.content)[0]
                    await event.message.channel.send(
                        f"{result[0]}fxtwitter{result[-1]}", reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True
                    )

                # Embeds composer - used for multiple images
                embeds: list[Embed] = []
                if content["images"]:
                    for image in content["images"]:
                        embeds.append(embed_generator(content, image))
                else:
                    embeds.append(embed_generator(content))

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
