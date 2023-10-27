from io import BytesIO

from aiohttp import ClientSession
from interactions import File


async def video_upload(url: str) -> File:
    # Download video from twitters cdn to discord File object
    async with ClientSession() as session:
        async with session.get(url) as response:
            file: bytes = await response.read()
            video: File = File(BytesIO(file), file_name="attachment.mp4")

    return video
