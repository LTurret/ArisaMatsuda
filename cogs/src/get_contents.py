from io import BytesIO
from re import findall
from re import search

from aiohttp import ClientSession
from interactions import File


async def get_contents(api_callback: dict) -> dict:
    
    # Initialize assets
    images: list[str] | list = []
    video: File | None = None
    media: list | None = None
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
                url: str = ""
                for asset in variants:
                    if asset["content_type"] == "video/mp4":
                        if asset["bitrate"] > best_bitrate:
                            best_bitrate = asset["bitrate"]
                            url = asset["url"]

                # Download video from twitters cdn to discord File object
                async with ClientSession() as session:
                    async with session.get(url) as response:
                        file: bytes = await response.read()
                        video: File = File(BytesIO(file), file_name="attachment.mp4")

        # Check is tweet contains multiple pictures
        if "media" in tweet_detail["entities"]: 
            for image in tweet_detail["entities"]["media"]:
                images.append(image["media_url_https"])

    except Exception:
        print("Ordinary method failed, try api.fxtwitter calling")
        try:
            # Abbreviation for data accessing
            tweet = tweet

            # Get assets
            favorite_count: int = tweet["likes"]
            retweet_count: int = tweet["retweets"]
            full_text = f'{tweet["text"]}'
            author: str = tweet["author"]["name"]
            screen_name: str = tweet["author"]["screen_name"]
            icon_url: str = tweet["author"]["avatar_url"]

            if "media" in tweet:
                media = tweet["media"]

                for image in media["photos"]:
                    images.append(image["url"])

        except Exception:
            raise Exception

    return {
        "images": images,
        "video": video,
        "full_text": full_text,
        "author": author,
        "screen_name": screen_name,
        "icon_url": icon_url,
        "favorite_count": favorite_count,
        "retweet_count": retweet_count,
    }
