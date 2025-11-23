import logging

from typing import Optional, List

from discord import Embed


class EmbedUtil:
    """
    The `EmbedUtil` class is responsible for creating and managing a queue of Discord Embed objects
    based on provided content. It automates the generation of embeds with support for both plain
    text and media-inclusive content. This class is useful for dynamically generating rich embed
    messages to be used in Discord bots.

    Attributes:
        embed_queue (list[Embed]): A list that stores the generated Embed objects.

    Parameters:
        content (Optional[dict]): A dictionary containing the content to be embedded.
                                  It should include keys like "full_text", "created_timestamp", "author",
                                  "screen_name", and optionally "images" and "icon_url".
        tweet_id (Optional[str]): The ID of the tweet or post to be linked in the embed.
        footer_text (Optional[str]): Custom footer text for the embed. Defaults to "樓梯的推特連結修復魔法".
    """

    def __init__(
        self,
        content: Optional[dict] = None,
        tweet_id: Optional[str] = None,
        footer_text: Optional[str] = "樓梯的推特連結修復魔法",
        original_link: Optional[str] = None,
        color: Optional[int] = 0x1DA0F2,
    ) -> None:
        """
        Initializes the EmbedUtil class and processes the provided content to generate Embed objects.

        - If the content contains images, multiple Embed objects are generated, one for each image.
        - If the content is plain text without images, a single Embed object is generated.

        Args:
            content (Optional[dict]): The content to be embedded.
            tweet_id (Optional[str]): The snowflake or ID of the tweet to be linked in the embed.
            footer_text (Optional[str]): Custom footer text for the embed.
        """
        logging.debug(f"↳ Class {__name__} created.")
        logging.debug(content)
        self.embed_queue: list[Embed] = []

        if content and "images" in content and content["images"]:
            logging.info(f"{__name__} Media contents processing.")

            for image in content["images"]:
                self.embed_queue.append(
                    self.__embed_generator(
                        content, tweet_id, image, original_link, footer_text, color
                    )
                )

        elif content:
            logging.info(f"{__name__} Plain content processing.")
            self.embed_queue.append(
                self.__embed_generator(
                    content=content,
                    tweet_id=tweet_id,
                    original_link=original_link,
                    footer_text=footer_text,
                    color=color,
                )
            )

    def __del__(self) -> None:
        """
        Destructor for the EmbedUtil class.
        """
        logging.debug(f"↳ Class {__name__} removed.")

    def __embed_generator(
        self,
        content: dict,
        tweet_id: str,
        media: Optional[str] = None,
        original_link: Optional[str] = None,
        footer_text: Optional[str] = None,
        color: int = 0x1DA0F2,
        icon_url: str = "https://abs.twimg.com/icons/apple-touch-icon-192x192.png",
        minimal: bool = True,
    ) -> Embed:
        """
        Generates a single Discord Embed object based on the provided content.

        This method creates an embed with a description, author, footer, and optionally includes fields
        for tweet statistics and an image if provided.

        Args:
            content (dict): The text to be embedded.
            tweet_id (str): The snowflake or ID of the tweet or post to be linked in the embed.
            media (Optional[str]): URL of an image to include in the embed.
            footer_text (Optional[str]): Custom footer text for the embed.
            color (int): The color of the embed. Defaults to Twitter's blue.
            icon_url (str): URL of the icon to be used in the footer. Defaults to Twitter's icon.
            minimal (bool): If False, includes fields for favorite and retweet counts. Defaults to True.

        Returns:
            Embed: A Discord Embed object configured with the provided content and options.
        """
        embed = Embed(
            color=color,
            url="https://twitter.com",
            description=content["full_text"],
            timestamp=content["created_timestamp"],
        )

        embed.set_author(
            name=f"{content['author']} (@{content['screen_name']})",
            url=f"https://twitter.com/{content['screen_name']}",
            icon_url=content["icon_url"],
        )

        embed.set_footer(text=footer_text, icon_url=icon_url)

        if not minimal:
            embed.add_field(
                name="愛心數", value=f"{int(content['favorite_count']):,}", inline=True
            )
            embed.add_field(
                name="轉推數", value=f"{int(content['retweet_count']):,}", inline=True
            )

        embed.add_field(
            name="推文傳送門",
            value=f"[點我！](https://fxtwitter.com/i/status/{tweet_id})",
            inline=True,
        )

        if original_link:
            embed.add_field(
                name="原始訊息", value=f"[原始貼文]({original_link})", inline=True
            )

        if media:
            embed.set_image(url=media)

        return embed
