import logging

from typing import Optional

from discord import Embed


class EmbedUtil:
    def __init__(self, content: Optional[dict] = None, tweet_id: Optional[str] = None, footer_text: Optional[str] = "樓梯的推特連結修復魔法"):
        self.embed_queue: list[Embed] = []

        # Simple constructor implementation, if the object contains arguments then auto genereate embeds
        # This feature likly to use **kwargs or *args
        if content and "images" in content and content["images"]:
            logging.info("Content media processing.")

            for image in content["images"]:
                self.embed_queue.append(self.__embed_generator(content, tweet_id, image, footer_text=footer_text))

        elif content:
            logging.info("Plain content processing.")
            self.embed_queue.append(self.__embed_generator(content, tweet_id, footer_text=footer_text))

    def __embed_generator(
        self,
        content: dict,
        tweet_id: str,
        media: Optional[str] = None,
        footer_text: Optional[str] = None,
        color: int = 0x1DA0F2,
        icon_url: str = "https://abs.twimg.com/icons/apple-touch-icon-192x192.png",
        minimal: bool = True,
    ) -> Embed:
        embed: Optional[list[Embed]] = Embed(color=color, url="https://twitter.com", description=content["full_text"], timestamp=content["created_timestamp"])

        embed.set_author(
            name=f"{content['author']} (@{content['screen_name']})", url=f"https://twitter.com/{content['screen_name']}", icon_url=content["icon_url"]
        )

        embed.set_footer(
            text=footer_text,
            icon_url=icon_url,
        )

        if not minimal:
            embed.add_field(name="愛心數", value=f'{int(content["favorite_count"]):3,d}', inline=True)
            embed.add_field(name="轉推數", value=f'{int(content["retweet_count"]):3,d}', inline=True)

        embed.add_field(name="推文傳送門", value=f"[點我！](https://fxtwitter.com/i/status/{tweet_id})", inline=True)

        if media:
            embed.set_image(url=media)

        logging.debug(f"(__embed_generator) embed = {embed}")
        return embed
