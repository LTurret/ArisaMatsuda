from re import search

from interactions import events
from interactions import listen
from interactions import Extension

class twitterFix(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_message_create(self, event: events.MessageCreate):
        if search("https://twitter.com/", event.message.content) and event.message.author != self.Arisa.user:
            head = search("https", event.message.content).start()
            parser = event.message.content[head+8:]
            await event.message.channel.send(f"### 連結修復魔法\nhttps://vx{parser}")
    
def setup(Arisa):
    twitterFix(Arisa)