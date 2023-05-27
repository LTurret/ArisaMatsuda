import interactions

class test(interactions.Extension):
    def __init__(self, Arisa):
        self.Arisa = Arisa

    @interactions.on_message_create
    async def test(self, ctx: interactions.SlashContext):
        print(ctx)

def setup(Arisa):
    test(Arisa)