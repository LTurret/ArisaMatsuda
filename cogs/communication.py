from io import BytesIO
from os import getenv

from aiohttp import ClientSession

from interactions import client
from interactions import listen
from interactions import message_context_menu
from interactions import modal_callback
from interactions import ContextMenuContext
from interactions import Extension
from interactions import File
from interactions import Message
from interactions import Modal
from interactions import ModalContext
from interactions import ParagraphText
from interactions.api.events import MessageCreate
from interactions.models.discord import channel


async def fetch(session: ClientSession, url: str) -> bytes | None:
    async with session.get(url) as response:
        file: bytes = await response.read()
        return file


class communication(Extension):
    def __init__(self, Arisa):
        self.Arisa: client = Arisa
        print(f" ↳ Extension {__name__} created")

    @message_context_menu(name="刪除訊息")
    async def delete(self, ctx: ContextMenuContext):
        message: Message = ctx.target
        await message.delete()
        await ctx.send(content="已刪除訊息", ephemeral=True)

    @message_context_menu(name="編輯訊息")
    async def delete(self, ctx: ContextMenuContext):
        modal = Modal(
            ParagraphText(label="Long Input Text", custom_id="long_text"),
            title="編輯訊息",
            custom_id="edit",
        )
        await ctx.send_modal(modal=modal)

    @modal_callback("my_modal")
    async def on_modal_answer(self, ctx: ModalContext, message: str):
        await ctx.send(f"Your text: {message}", ephemeral=True)

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
            content: str = f"**({str(event.message.author)})**　{event.message.content}"

            # Send message
            if event.message.author != self.Arisa.user:
                entry: channel = self.Arisa.get_channel(channel_manifest[event.message.channel.id])
                if "files" in locals():
                    await entry.send(content=content, files=files)
                else:
                    await entry.send(content=content)


def setup(Arisa):
    communication(Arisa)
