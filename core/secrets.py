import json

def tokens() -> list:
    with open("./core/config/token.json", "r") as token:
        token = json.load(token)

        bot = token["bot_token"]

    TokenSet = {
        "bot": bot
    }

    return TokenSet