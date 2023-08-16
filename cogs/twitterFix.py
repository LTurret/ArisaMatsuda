from io import BytesIO
from json import dump
from json import dumps
from re import findall
from re import search
from time import time
from urllib.parse import quote

from aiohttp import ClientSession
from interactions import events
from interactions import listen
from interactions import AllowedMentions
from interactions import Embed
from interactions import Extension
from interactions import File


class twitterFix(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: events.MessageCreate):
        if event.message.author != self.Arisa.user:

            async def get_tokens() -> dict:
                async with ClientSession() as session:
                    async with session.get("https://twitter.com") as response:
                        response = await response.text()
                        js_url: str = findall(r"https://abs.twimg.com/responsive-web/client-web-legacy/main.[^\.]+.js", response)[0]
                    async with session.get(js_url) as mainjs:
                        mainjs = await mainjs.text()
                        bearer_token: str = findall(r'AAAAAAAAA[^"]+', mainjs)[0]

                headers = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "te": "trailers", "authorization": f"Bearer {bearer_token}"}

                async with ClientSession(headers=headers) as session:
                    async with session.post("https://api.twitter.com/1.1/guest/activate.json") as response:
                        guest_token: str = await response.json()
                        guest_token = guest_token["guest_token"]

                return {"bearer_token": bearer_token, "guest_token": guest_token}

            def fetch_tweet(tweetId: int, features: dict, variables: dict, query_id_token: str = "0hWvDhmW8YQ-S_ib3azIrw") -> str:
                variables: dict = {**variables}
                variables["tweetId"] = tweetId

                api_url: str = ""
                api_url += f"https://twitter.com/i/api/graphql/{query_id_token}"
                api_url += f"/TweetResultByRestId?variables={quote(dumps(variables))}&features={quote(dumps(features))}"

                return api_url

            async def get_contents(api_callback) -> dict:
                body_post: dict = api_callback["data"]["tweetResult"]["result"]["legacy"]
                media: list | None = None
                media_first: str | None = None
                media_video: str | None = None
                full_text: str | None = None

                favorite_count: int = body_post["favorite_count"]
                retweet_count: int = body_post["retweet_count"]

                user_results_legacy: dict = api_callback["data"]["tweetResult"]["result"]["core"]["user_results"]["result"]["legacy"]
                author: str = user_results_legacy["name"]
                screen_name: str = user_results_legacy["screen_name"]
                icon_url: str = user_results_legacy["profile_image_url_https"]

                if "media" in body_post["entities"]:
                    media = body_post["entities"]["media"]
                    media_first = body_post["entities"]["media"][0]["media_url_https"]
                    if "video_info" in body_post["extended_entities"]["media"][0]:
                        async with ClientSession() as session:
                            async with session.get(body_post["extended_entities"]["media"][0]["video_info"]["variants"][-1]["url"]) as response:
                                file: bytes = await response.read()
                        file = File(BytesIO(file), file_name="attachment.mp4")
                        media_video = file

                if "full_text" in body_post:
                    start = search(r"https:\/\/t.co\/", body_post["full_text"]).start()
                    full_text = body_post["full_text"][: start - 1]

                return {
                    "media": media,
                    "media_first": media_first,
                    "media_video": media_video,
                    "full_text": full_text,
                    "author": author,
                    "screen_name": screen_name,
                    "icon_url": icon_url,
                    "favorite_count": favorite_count,
                    "retweet_count": retweet_count,
                }

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
            variables: dict = {"includePromotedContent": False, "withCommunity": False, "withVoice": False}
            tokens: dict = {**(await get_tokens())}

            if search(r"^https://twitter.com/", event.message.content) and search(r"/status/", event.message.content):
                tweetId = findall(r"\/[0-9][^\?|\/]+", event.message.content)[0][1:]
                api_url: str = fetch_tweet(tweetId, features, variables)
                headers = {"authorization": f"Bearer {tokens['bearer_token']}", "x-guest-token": tokens["guest_token"]}
                async with ClientSession(headers=headers) as session:
                    async with session.get(api_url) as response:
                        api_callback = await response.json()
                content: dict = {**(await get_contents(api_callback))}
                embed = Embed(description=content["full_text"], color=0x1DA0F2, timestamp=time())
                embed.set_author(
                    name=f"{content['author']} (@{content['screen_name']})", url=f"https://twitter.com/{content['screen_name']}", icon_url=content["icon_url"]
                )
                embed.set_image(content["media_first"])
                embed.add_field(name="Likes", value=content["favorite_count"], inline=True)
                embed.add_field(name="Retweets", value=content["retweet_count"], inline=True)
                embed.set_footer(
                    text="樓梯的推特連結修復魔法",
                    icon_url="https://images-ext-1.discordapp.net/external/bXJWV2Y_F3XSra_kEqIYXAAsI3m1meckfLhYuWzxIfI/https/abs.twimg.com/icons/apple-touch-icon-192x192.png",
                )

                # credit - kenneth (https://discord.com/channels/789032594456576001/1141430904644964412)
                if content["media_video"]:
                    await event.message.channel.send(
                        files=[content["media_video"]], embeds=embed, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True
                    )
                else:
                    await event.message.channel.send(embeds=embed, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True)


def setup(Arisa):
    twitterFix(Arisa)
