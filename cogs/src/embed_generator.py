from time import time

from interactions import Embed


def embed_generator(content: dict, media: str, url: str = "https://arisahi.me", color: hex = 0x1DA0F2) -> Embed:
    embed: Embed = Embed(description=content["full_text"], color=color, timestamp=time(), url=url)
    embed.set_author(
        name=f"{content['author']} (@{content['screen_name']})",
        url=f"https://twitter.com/{content['screen_name']}",
        icon_url=content["icon_url"],
    )
    embed.set_footer(
        text="樓梯的推特連結修復魔法",
        icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png",
    )
    embed.set_image(media)
    return embed
