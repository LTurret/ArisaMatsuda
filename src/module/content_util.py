import logging

from datetime import datetime
from io import BytesIO
from pathlib import Path
from re import findall, search
from typing import List, Optional
from aiohttp import ClientSession

from discord import File


class ContentUtil:
    """
    The `ContentUtil` class is responsible for retrieving and processing content from social media platforms,
    specifically Twitter and fxTwitter. It can handle both images and videos, preparing them for use in Discord bots.

    Methods:
        get_contents(api_callback: dict, host: str): Retrieves content based on the provided host (e.g., "twitter" or "fx").
        __video_upload(url: str): Download a video from the provided URL and prepares it for upload to Discord.
        __by_twitter(api_callback: dict): Processes Twitter-specific content.
        __by_fx(api_callback: dict): Processes fxTwitter-specific content.
    """

    def __init__(self, file: Optional[Path] = None) -> File:
        """
        Initializes the ContentUtil class.

        If `file` is provided, it will be used to create a Discord File object.
        """
        logging.debug(f"↳ Class {__name__} created.")

        if file is not None:
            return File(BytesIO(file), filename="attachment.mp4")

    def __del__(self) -> None:
        """
        Destructor for the ContentUtil class.
        """
        logging.debug(f"↳ Class {__name__} removed.")

    async def get_contents(self, api_callback: dict, host: str = "fx") -> dict:
        """
        Retrieves and processes content based on the host platform.

        Parameters:
            api_callback (dict): The API response data to be processed.
            host (str): The platform from which the content is being retrieved. Defaults to "fx".

        Returns:
            dict: A dictionary containing processed content, including text, images, and videos.
        """
        service_manifest: dict = {"twitter": self.__by_twitter, "fx": self.__by_fx}
        content: dict = await service_manifest[host](api_callback)
        return content

    async def __video_upload(self, url: str) -> File:
        """
        Downloads a video from the provided URL and prepares it for upload to Discord.

        Parameters:
            url (str): The URL of the video to be downloaded.

        Returns:
            File: A Discord File object containing the video data.
        """
        async with ClientSession() as session:
            async with session.get(url) as response:
                file: bytes = await response.read()
                video: File = File(BytesIO(file), filename="attachment.mp4")
        return video

    async def __by_twitter(self, api_callback: dict) -> dict:
        """
        Processes Twitter-specific content from the API callback.

        This method extracts the necessary details from a Twitter API response, including
        tweet text, images, videos, and metadata such as the author, like count, and retweet count.

        Args:
            api_callback (dict): The API response data from Twitter.

        Returns:
            dict: A dictionary containing the processed Twitter content.
        """
        tweet_detail: dict = api_callback["data"]["tweetResult"]["result"]["legacy"]
        user_results_legacy: dict = api_callback["data"]["tweetResult"]["result"][
            "core"
        ]["user_results"]["result"]["legacy"]

        # Initialize fields
        author: str = user_results_legacy["author"]["screen_name"]
        screen_name: str = user_results_legacy["author"]["screen_name"]
        icon_url: str = user_results_legacy["author"]["avatar_url"]
        full_text: str = user_results_legacy["text"]
        favorite_count: int = tweet_detail["likes"]
        retweet_count: int = tweet_detail["retweets"]
        created_timestamp: int = 0  # Not plan to fix

        images: list[str] = []
        videos: list[File] = []

        # Extract tweet content text
        if "full_text" in tweet_detail:
            full_text = tweet_detail["full_text"]
            start: int = -1

            # Shadowing image URL in tweet text
            if findall(r"https:\/\/t.co\/.+", full_text):
                match_pop: str = findall(r"https:\/\/t.co\/.+", full_text)[-1]
                start = search(match_pop, full_text).start()

            full_text = full_text[:start]

        # Extract tweet media
        if "extended_entities" in tweet_detail:
            if "video_info" in tweet_detail["extended_entities"]["media"][0]:
                variants: dict = tweet_detail["extended_entities"]["media"][0][
                    "video_info"
                ]["variants"]

                # Find best bitrate
                upper_bitrate: int = 0
                for asset in variants:
                    if asset["content_type"] == "video/mp4":
                        if asset["bitrate"] > upper_bitrate:
                            upper_bitrate = asset["bitrate"]
                        videos.append(await self.__video_upload(asset["url"]))

            # Only check pictures when tweet does not contain any video
            else:
                # Check if tweet contains multiple pictures
                if "media" in tweet_detail["entities"]:
                    for image in tweet_detail["entities"]["media"]:
                        images.append(image["media_url_https"])

        return {
            "images": images,
            "videos": videos,
            "full_text": full_text,
            "author": author,
            "screen_name": screen_name,
            "icon_url": icon_url,
            "favorite_count": favorite_count,
            "retweet_count": retweet_count,
            "created_timestamp": created_timestamp,
        }

    async def __by_fx(self, api_callback: dict) -> dict:
        """
        Processes fxTwitter-specific content from the API callback.

        This method extracts the necessary details from an fxTwitter API response, including
        tweet text, images, videos, and metadata such as the author, like count, and retweet count.

        Args:
            api_callback (dict): The API response data from fxTwitter.

        Returns:
            dict: A dictionary containing the processed fxTwitter content.
        """
        tweet: dict = api_callback["tweet"]

        # Initialize fields
        author: str = tweet["author"]["screen_name"]
        screen_name: str = tweet["author"]["screen_name"]
        icon_url: str = tweet["author"]["avatar_url"]
        full_text: str = tweet["text"]
        favorite_count: int = tweet["likes"]
        retweet_count: int = tweet["retweets"]
        created_timestamp: datetime = datetime.fromtimestamp(tweet["created_timestamp"])

        images: list[str] = []
        videos: list[File] = []

        if "media" in tweet:
            media = tweet["media"]

            if "videos" in media:
                for raw_video in media["videos"]:
                    logging.info(f"{__name__}: Uploading video asset to Discord CDN.")
                    videos.append(await self.__video_upload(raw_video["url"]))

            if "photos" in media:
                for image in media["photos"]:
                    logging.info(f"{__name__}: Embedding images.")
                    images.append(image["url"])

        return {
            "author": author,
            "screen_name": screen_name,
            "icon_url": icon_url,
            "full_text": full_text,
            "images": images,
            "videos": videos,
            "favorite_count": favorite_count,
            "retweet_count": retweet_count,
            "created_timestamp": created_timestamp,
        }
