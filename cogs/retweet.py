# from interactions import events
from interactions import listen
# from interactions import AllowedMentions
# from interactions import Embed
from interactions import Extension
# from interactions import File
from interactions import IntervalTrigger
from interactions import Task


class retweet(Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa
        print(f" ↳ Extension {__name__} created")

    @listen()
    async def on_startup(self):
        self.retweet.start()

    @Task.create(IntervalTrigger(seconds=2))
    async def retweet(self):
        print("hello world")


def setup(Arisa):
    retweet(Arisa)