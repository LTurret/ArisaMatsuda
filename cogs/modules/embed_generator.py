from interactions import Embed


def embed_generator(content: dict, media: str | None = None, tweetId: str | None = None, color: hex = 0x1DA0F2) -> Embed:
    embed: Embed = Embed(description=content["full_text"], color=color, timestamp=content["created_timestamp"], url="https://twitter.com")
    embed.set_author(
        name=f"{content['author']} (@{content['screen_name']})",
        url=f"https://twitter.com/{content['screen_name']}",
        icon_url=content["icon_url"],
    )
    embed.set_footer(
        text="樓梯的推特連結修復魔法",
        icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png",
    )
    embed.add_field(name="愛心數", value=f'{int(content["favorite_count"]):3,d}', inline=True)
    embed.add_field(name="轉推數", value=f'{int(content["retweet_count"]):3,d}', inline=True)
    embed.add_field(name="推文傳送門", value=f"[點我！](https://fxtwitter.com/i/status/{tweetId})", inline=True)

    if media:
        embed.set_image(media)

    return embed
