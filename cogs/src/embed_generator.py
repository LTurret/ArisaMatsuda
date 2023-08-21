from time import time

from interactions import Embed


def embed_generator(content: dict, media: str, url: str = "https://arisahi.me", color: hex = 0x1DA0F2) -> Embed:
    embed = Embed(description=content["full_text"], color=color, timestamp=time(), url=url)
    embed.set_image(media)
    return embed
