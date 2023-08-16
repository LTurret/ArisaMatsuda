from io import BytesIO
from os import getenv

from aiohttp import ClientSession

from interactions import listen
from interactions import Extension
from interactions import File
from interactions.api.events import MessageCreate
from interactions.models.discord import channel


async def fetch(session: ClientSession, url: str) -> bytes | None:
    async with session.get(url) as response:
        file: bytes = await response.read()
        return file


class communication(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: MessageCreate):
        bi_channel_1: int = int(getenv("bi-channel_1"))
        bi_channel_2: int = int(getenv("bi-channel_2"))

        channel_manifest: dict = {bi_channel_1: bi_channel_2, bi_channel_2: bi_channel_1}

        # Attachments handler
        if len(event.message.attachments) != 0:
            files: list[bytes] = []
            for attachment in event.message.attachments:
                async with ClientSession() as session:
                    file = await fetch(session, attachment.url)
                    files.append(File(BytesIO(file), file_name=attachment.filename))

        # Channel filter
        if int(event.message.channel.id) == bi_channel_1 or int(event.message.channel.id) == bi_channel_2:
            content: str = "**("

            # Give a specify member special identity
            if str(event.message.author) == "ペットリー#4222":
                content += "🐑 "
            content += f"{str(event.message.author)})**　{event.message.content}"

            # Send message
            if event.message.author != self.Arisa.user:
                entry: channel = self.Arisa.get_channel(channel_manifest[event.message.channel.id])
                if "files" in locals():
                    await entry.send(content=content, files=files)
                else:
                    await entry.send(content=content)


def setup(Arisa):
    communication(Arisa)
