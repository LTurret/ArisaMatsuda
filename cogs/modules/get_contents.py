from re import findall
from re import search
from time import time

from interactions import File

from cogs.modules.video_upload import video_upload


async def get_contents(api_callback: dict, host: str = "fx") -> dict:
    service_manifest: dict = {"twitter": by_twitter, "fx": by_fx}
    content: dict = await service_manifest[host](api_callback)
    return content


async def by_twitter(api_callback: dict):
    # Initialize assets
    author: str = ""
    screen_name: str = ""
    icon_url: str = ""
    full_text: str | None = None
    images: list[str] | list = []
    videos: list[File] | list = []
    favorite_count: int = -1
    retweet_count: int = -1
    created_timestamp: int = time()

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
                videos.append(await video_upload(asset["url"]))

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


async def by_fx(api_callback: dict):
    # Initialize assets
    author: str = ""
    screen_name: str = ""
    icon_url: str = ""
    full_text: str | None = None
    images: list[str] | list = []
    videos: list[File] | list = []
    favorite_count: int = -1
    retweet_count: int = -1
    created_timestamp: int = 0

    # Abbreviation for data accessing
    tweet = api_callback["tweet"]

    # Get assets
    author = tweet["author"]["name"]
    screen_name = tweet["author"]["screen_name"]
    icon_url = tweet["author"]["avatar_url"]
    full_text = f'{tweet["text"]}'
    favorite_count = tweet["likes"]
    retweet_count = tweet["retweets"]
    created_timestamp = tweet["created_timestamp"]

    if "media" in tweet:
        media = tweet["media"]

        if "videos" in media:
            tasks: list = []
            for raw_video in media["videos"]:
                videos.append(await video_upload(raw_video["url"]))

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
