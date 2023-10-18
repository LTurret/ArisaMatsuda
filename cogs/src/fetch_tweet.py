from re import findall

from json import dumps
from urllib.parse import quote

from aiohttp import ClientSession


async def fetch_tweet(tokens: dict, tweetId: int, query_id_token: str = "0hWvDhmW8YQ-S_ib3azIrw") -> dict:
    features: dict = {
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "tweetypie_unmention_optimization_enabled": True,
        "vibe_api_enabled": False,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": False,
        "longform_notetweets_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "interactive_text_enabled": False,
        "responsive_web_twitter_blue_verified_badge_is_enabled": True,
        "responsive_web_text_conversations_enabled": False,
        "longform_notetweets_richtext_consumption_enabled": False,
        "responsive_web_enhance_cards_enabled": False,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_media_download_video_enabled": False,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "creator_subscriptions_tweet_preview_api_enabled": True,
    }
    variables: dict = {
        "includePromotedContent": False,
        "withCommunity": False,
        "withVoice": False,
    }

    variables_reference: dict = {**variables}
    variables_reference["tweetId"] = tweetId

    root: str = "https://twitter.com/i/api"
    prefix: str = "graphql"
    query: str = f"{query_id_token}"
    suffix: str = f"TweetResultByRestId?variables={quote(dumps(variables_reference))}&features={quote(dumps(features))}"
    api_url: str = f"{root}/{prefix}/{query}/{suffix}"

    headers: dict = {
        "authorization": f"Bearer {tokens['bearer_token']}",
        "x-guest-token": tokens["guest_token"],
    }

    async with ClientSession(headers=headers) as session:
        async with session.get(api_url) as response:
            callback: dict = await response.json()

    if findall(r"NsfwLoggedOut", str(callback)):
        url: str = f"https://api.fxtwitter.com/i/status/{tweetId}"
        async with ClientSession() as session:
            async with session.get(url) as response:
                callback: dict = await response.json()

    return callback
