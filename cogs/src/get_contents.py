from re import findall
from re import search

from interactions import File

from cogs.src.video_upload import video_upload


async def get_contents(api_callback: dict) -> dict:
    # Initialize assets
    images: list[str] | list = []
    videos: list[File] | list = []
    full_text: str | None = None
    author: str = ""
    screen_name: str = ""
    icon_url: str = ""
    favorite_count: int = -1
    retweet_count: int = -1

    try:
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

    except Exception:
        try:
            # Abbreviation for data accessing
            tweet = api_callback["tweet"]

            # Get assets
            favorite_count = tweet["likes"]
            retweet_count = tweet["retweets"]
            full_text = f'{tweet["text"]}'
            author = tweet["author"]["name"]
            screen_name = tweet["author"]["screen_name"]
            icon_url = tweet["author"]["avatar_url"]

            if "media" in tweet:
                media = tweet["media"]

                if "videos" in media:
                    for raw_video in media["videos"]:
                        videos.append(await video_upload(raw_video["url"]))

                if "photos" in media:
                    for image in media["photos"]:
                        images.append(image["url"])

        except Exception as exception:
            raise exception

    return {
        "images": images,
        "videos": videos,
        "full_text": full_text,
        "author": author,
        "screen_name": screen_name,
        "icon_url": icon_url,
        "favorite_count": favorite_count,
        "retweet_count": retweet_count,
    }
