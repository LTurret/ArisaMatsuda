from interactions import listen
from interactions import Extension
from interactions.api.events import MessageCreate

class communication(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa

    @listen()
    async def on_message_create(self, event: MessageCreate):
        entry_anna = await self.Arisa.fetch_channel(695508789327298570)
        entry_arisa = await self.Arisa.fetch_channel(1052268807038709846)

        if event.message.author != self.Arisa.user:
            if await entry_arisa.fetch_message(event.message):
                await entry_anna.send(event.message.content)
            else:
                await entry_arisa.send(event.message.content)

def setup(Arisa):
    communication(Arisa)
