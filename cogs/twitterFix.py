from re import search
from time import time

from interactions import events
from interactions import listen
from interactions import AllowedMentions
from interactions import Embed
from interactions import Extension

from cogs.src.embed_generator import embed_generator
from cogs.src.fetch_tweet import fetch_tweet
from cogs.src.get_contents import get_contents
from cogs.src.get_tokens import get_tokens


class twitterFix(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: events.MessageCreate):
        if event.message.author != self.Arisa.user:
            if search(r"https://twitter\.com/.+/\d+[^?]", event.message.content):
                emoji = await self.Arisa.fetch_custom_emoji(1089582594833789028, 339368837356978187, force=True)
                await event.message.add_reaction(emoji)

    @listen()
    async def on_message_react(self, event: events.MessageReactionAdd):
        if event.message.reactions[0].me and event.message.reactions[0].count > 1:
            # Clear reactions
            await event.message.reactions[0].remove()

            # API headers
            tokens: dict = {**(await get_tokens())}

            # Find activation
            if search(r"https\:\/\/[x|twitter]+\.com\/.+\/[.\d^\?]+", event.message.content):
                tweetId = search(r"status\/([0-9][^\?|\/]+)", event.message.content).group(1)
                api_callback: dict = await fetch_tweet(tokens, tweetId)

                try:
                    content: dict = {**(await get_contents(api_callback))}
                    embeds: list = []

                    # Embeds composer - used for multiple images
                    if content["images"]:
                        for image in content["images"]:
                            embeds.append(embed_generator(content, image))
                    else:
                        init_embed: Embed = Embed(description=content["full_text"], color=0x1DA0F2, timestamp=time(), url="https://arisahi.me")
                        init_embed.set_author(
                            name=f"{content['author']} (@{content['screen_name']})",
                            url=f"https://twitter.com/{content['screen_name']}",
                            icon_url=content["icon_url"],
                        )
                        init_embed.set_footer(
                            text="樓梯的推特連結修復魔法",
                            icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png",
                        )
                        embeds.append(init_embed)

                    # Send embed
                    # credit - kenneth (https://discord.com/channels/789032594456576001/1141430904644964412)
                    if content["video"] is not None:
                        await event.message.channel.send(
                            files=content["video"], embeds=embeds, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True
                        )
                    else:
                        await event.message.channel.send(embeds=embeds, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True)
                except FileNotFoundError:
                    await event.message.channel.send(
                        """```diff\n- Request failed\nprobably due to nsfw content, check if callback is {"reason": "NsfwLoggedOut"}```"""
                    )


def setup(Arisa):
    twitterFix(Arisa)
