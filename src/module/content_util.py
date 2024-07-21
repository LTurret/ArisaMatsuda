import logging

from datetime import datetime
from io import BytesIO
from re import findall, search
from typing import Optional

from aiohttp import ClientSession
from discord import File


class ContentUtil:
    def __init__(self):
        logging.info(f" ↳ Extension {__name__} loaded")

    async def get_contents(self, api_callback: dict, host: str = "fx") -> dict:
        service_manifest: dict = {"twitter": self.__by_twitter, "fx": self.__by_fx}
        content: dict = await service_manifest[host](api_callback)
        return content

    async def video_upload(url: str) -> File:
        async with ClientSession() as session:
            async with session.get(url) as response:
                file: bytes = await response.read()
                video: File = File(BytesIO(file), file_name="attachment.mp4")
        return video

    async def __by_twitter(self, api_callback: dict) -> dict:
        # Initialize assets
        author: str = ""
        screen_name: str = ""
        icon_url: str = ""
        full_text: str | None = None
        images: list[str] | list = []
        videos: list[File] | list = []
        favorite_count: int = -1
        retweet_count: int = -1
        created_timestamp: datetime = datetime.now()

        # Abbreviations for data accessing
        tweet_detail: dict = api_callback["data"]["tweetResult"]["result"]["legacy"]
        user_results_legacy: dict = api_callback["data"]["tweetResult"]["result"]["core"]["user_results"]["result"]["legacy"]

        # Get assets
        author = user_results_legacy["name"]
        screen_name = user_results_legacy["screen_name"]
        icon_url = user_results_legacy["profile_image_url_https"]
        favorite_count = tweet_detail["favorite_count"]
        retweet_count = tweet_detail["retweet_count"]

        # Extract tweet content text
        if "full_text" in tweet_detail:
            full_text: str = tweet_detail["full_text"]
            start: int = -1

            # Shadowing image URL in tweet text
            if findall(r"https:\/\/t.co\/.+", full_text):
                match_pop: str = findall(r"https:\/\/t.co\/.+", full_text)[-1]
                start: int = search(match_pop, full_text).start()

            full_text = full_text[:start]

        # Extract tweet medias
        if "extended_entities" in tweet_detail:
            if "video_info" in tweet_detail["extended_entities"]["media"][0]:
                variants: dict = tweet_detail["extended_entities"]["media"][0]["video_info"]["variants"]

                # find best bitrate
                best_bitrate: int = 0
                for asset in variants:
                    if asset["content_type"] == "video/mp4":
                        if asset["bitrate"] > best_bitrate:
                            best_bitrate = asset["bitrate"]
                    videos.append(await self.video_upload(asset["url"]))

            # Only check pictures when tweet is not contain any video
            else:
                # Check is tweet contains multiple pictures
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
        # Abbreviation for data accessing
        tweet: dict = api_callback["tweet"]
        
        # Initialize assets
        author: str = tweet["author"]["screen_name"]
        screen_name: str = tweet["author"]["screen_name"]
        icon_url: str = tweet["author"]["avatar_url"]
        full_text: Optional[str] = tweet["text"]
        favorite_count: int = tweet["likes"]
        retweet_count: int = tweet["retweets"]
        created_timestamp: Optional[int | datetime] = datetime.fromtimestamp(tweet["created_timestamp"])

        images: list[str] = []
        videos: list[File] = []
        
        if "media" in tweet:
            media = tweet["media"]

            if "videos" in media:
                for raw_video in media["videos"]:
                    videos.append(await self.video_upload(raw_video["url"]))

            if "photos" in media:
                for image in media["photos"]:
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
