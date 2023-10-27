from time import time

from interactions import Embed


def embed_generator(
    content: dict,
    media: str | None = None,
    tweetId: str | None = None,
    url: str = "https://arisahi.me",
    color: hex = 0x1DA0F2,
    footer_icon: str = "https://abs.twimg.com/icons/apple-touch-icon-192x192.png",
    attach_origin_url: bool = False,
) -> Embed:
    embed: Embed = Embed(description=content["full_text"], color=color, timestamp=time(), url=url)
    embed.set_author(
        name=f"{content['author']} (@{content['screen_name']})",
        url=f"https://twitter.com/{content['screen_name']}",
        icon_url=content["icon_url"],
    )
    embed.set_footer(
        text="樓梯的推特連結修復魔法",
        icon_url=footer_icon,
    )

    if media:
        embed.set_image(media)

    if attach_origin_url:
        embed.add_field(name="原文傳送門", value=f"[點我](https://twitter.com/i/status/{tweetId})", inline=False)

    return embed
