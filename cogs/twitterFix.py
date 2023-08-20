from io import BytesIO
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
            # Token handler
            async def get_tokens() -> dict:
                async with ClientSession() as session:
                    async with session.get("https://twitter.com") as response:
                        response: str = await response.text()
                        js_url: str = findall(r"https://abs.twimg.com/responsive-web/client-web-legacy/main.[^\.]+.js", response)[0]
                    async with session.get(js_url) as mainjs:
                        mainjs: str = await mainjs.text()
                        bearer_token: str = findall(r'AAAAAAAAA[^"]+', mainjs)[0]

                headers: dict = {"accept": "*/*", "accept-encoding": "gzip, deflate, br", "te": "trailers", "authorization": f"Bearer {bearer_token}"}

                async with ClientSession(headers=headers) as session:
                    async with session.post("https://api.twitter.com/1.1/guest/activate.json") as response:
                        guest_token: str = await response.json()
                        guest_token = guest_token["guest_token"]

                return {"bearer_token": bearer_token, "guest_token": guest_token}

            # Tweet fetch
            async def fetch_tweet(tweetId: int, features: dict, variables: dict, query_id_token: str = "0hWvDhmW8YQ-S_ib3azIrw") -> dict:
                variables: dict = {**variables}
                variables["tweetId"] = tweetId

                api_url: str = ""
                root: str = ""
                api_url += f"https://twitter.com/i/api/graphql/{query_id_token}"
                api_url += f"/TweetResultByRestId?variables={quote(dumps(variables))}&features={quote(dumps(features))}"

                headers: dict = {"authorization": f"Bearer {tokens['bearer_token']}", "x-guest-token": tokens["guest_token"]}

                async with ClientSession(headers=headers) as session:
                    async with session.get(api_url) as response:
                        callback: dict = await response.json()

                return callback

            # Get contents from API-callback
            async def get_contents(api_callback: dict) -> dict:
                tweet_detail: dict = api_callback["data"]["tweetResult"]["result"]["legacy"]
                images: list = []
                video: File | None = None
                media: list | None = None
                full_text: str | None = None

                favorite_count: int = tweet_detail["favorite_count"]
                retweet_count: int = tweet_detail["retweet_count"]

                user_results_legacy: dict = api_callback["data"]["tweetResult"]["result"]["core"]["user_results"]["result"]["legacy"]
                author: str = user_results_legacy["name"]
                screen_name: str = user_results_legacy["screen_name"]
                icon_url: str = user_results_legacy["profile_image_url_https"]

                # Extract tweet content text
                if "full_text" in tweet_detail:
                    full_text: str = tweet_detail["full_text"]
                    start: int = -1

                    if findall(r"https:\/\/t.co\/.+", full_text):
                        match_pop: str = findall(r"https:\/\/t.co\/.+", full_text)[-1]
                        start: int = search(match_pop, full_text).start()

                    full_text = full_text[:start]

                # Extract tweet medias
                if "extended_entities" in tweet_detail:
                    if "video_info" in tweet_detail["extended_entities"]["media"][0]:
                        async with ClientSession() as session:
                            async with session.get(tweet_detail["extended_entities"]["media"][0]["video_info"]["variants"][-1]["url"]) as response:
                                file: bytes = await response.read()
                                video = File(BytesIO(file), file_name="attachment.mp4")

                if "media" in tweet_detail["entities"]:
                    media: list = tweet_detail["entities"]["media"]
                    for image in media:
                        images.append(image["media_url_https"])

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

            def embed_generator(content: dict, media: str, url: str = "https://arisahi.me") -> Embed:
                embed = Embed(description=content["full_text"], color=0x1DA0F2, timestamp=time(), url=url)
                embed.set_author(
                    name=f"{content['author']} (@{content['screen_name']})", url=f"https://twitter.com/{content['screen_name']}", icon_url=content["icon_url"]
                )
                embed.set_image(media)
                embed.add_field(name="Likes", value=content["favorite_count"], inline=True)
                embed.add_field(name="Retweets", value=content["retweet_count"], inline=True)
                embed.set_footer(
                    text="樓梯的推特連結修復魔法",
                    icon_url="https://images-ext-1.discordapp.net/external/bXJWV2Y_F3XSra_kEqIYXAAsI3m1meckfLhYuWzxIfI/https/abs.twimg.com/icons/apple-touch-icon-192x192.png",
                )
                return embed

            # API headers
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

            # Find activation
            if search(r"https://twitter.com/", event.message.content) and search(r"/status/", event.message.content):
                tweetId = search(r"status\/([0-9][^\?|\/]+)", event.message.content).group(1)
                api_callback: dict = await fetch_tweet(tweetId, features, variables)
                content: dict = {**(await get_contents(api_callback))}
                init_embed: Embed = Embed(description=content["full_text"], color=0x1DA0F2, timestamp=time(), url="https://arisahi.me")
                init_embed.set_author(
                    name=f"{content['author']} (@{content['screen_name']})", url=f"https://twitter.com/{content['screen_name']}", icon_url=content["icon_url"]
                )
                init_embed.add_field(name="Likes", value=content["favorite_count"], inline=True)
                init_embed.add_field(name="Retweets", value=content["retweet_count"], inline=True)
                init_embed.set_footer(
                    text="樓梯的推特連結修復魔法",
                    icon_url="https://abs.twimg.com/icons/apple-touch-icon-192x192.png",
                )

                embeds: list = [init_embed]

                if content["images"]:
                    for image in content["images"]:
                        embeds.append(embed_generator(content, image))

                # Send embed
                # credit - kenneth (https://discord.com/channels/789032594456576001/1141430904644964412)
                if content["video"] is not None:
                    await event.message.channel.send(
                        files=content["video"], embeds=embeds, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True
                    )
                else:
                    await event.message.channel.send(embeds=embeds, reply_to=event.message, allowed_mentions=AllowedMentions.none(), silent=True)


def setup(Arisa):
    twitterFix(Arisa)
