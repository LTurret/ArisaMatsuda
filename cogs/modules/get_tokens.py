from re import findall

from aiohttp import ClientSession


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
            guest_token: str = guest_token["guest_token"]

    return {"bearer_token": bearer_token, "guest_token": guest_token}
