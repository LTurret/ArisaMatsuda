import interactions

class role(interactions.Extension):
    def __init__(self, ArisaInteraction):
        self.ArisaInteraction = ArisaInteraction

    @interactions.extension_command(
        name = "role",
        description = "問亞利沙",
        scope = 1052268806166294609
    )
    async def role(self, ctx: interactions.CommandContext):
        role_verified = interactions.Button(
            style = interactions.ButtonStyle.PRIMARY,
            label = "Verified",
            custom_id = "role_verified"
        )
        role_nsfw = interactions.Button(
            style = interactions.ButtonStyle.SECONDARY,
            label = "NSFW",
            custom_id = "role_nsfw"
        )
        role_programmer = interactions.Button(
            style = interactions.ButtonStyle.SECONDARY,
            label = "Programmer",
            custom_id = "role_programmer"
        )

        row = interactions.ActionRow(components=[role_nsfw, role_programmer])

        await ctx.send(content="身分組管理v1.0", components=[[role_verified], row])

    @interactions.extension_component("role_verified")
    async def role_action_verified(self, ctx):
        if any(list(map(lambda role_id: role_id == 1052268806166294610, ctx.author.roles))):
            await ctx.member.remove_role(role=1052268806166294610, guild_id=1052268806166294609)
            await ctx.send(content="已解除認證", ephemeral=True)
        else:
            await ctx.member.add_role(role=1052268806166294610, guild_id=1052268806166294609)
            await ctx.send(content="已認證", ephemeral=True)

    @interactions.extension_component("role_nsfw")
    async def role_action_nsfw(self, ctx):
        if any(list(map(lambda role_id: role_id == 1052268806166294611, ctx.author.roles))):
            await ctx.member.remove_role(role=1052268806166294611, guild_id=1052268806166294609)
            await ctx.send(content="已解除身分組", ephemeral=True)
        else:
            await ctx.member.add_role(role=1052268806166294611, guild_id=1052268806166294609)
            await ctx.send(content="已加入身分組", ephemeral=True)

    @interactions.extension_component("role_programmer")
    async def role_action_programmer(self, ctx):
        if any(list(map(lambda role_id: role_id == 1052268806166294614, ctx.author.roles))):
            await ctx.member.remove_role(role=1052268806166294614, guild_id=1052268806166294609)
            await ctx.send(content="已解除身分組", ephemeral=True)
        else:
            await ctx.member.add_role(role=1052268806166294614, guild_id=1052268806166294609)
            await ctx.send(content="已加入身分組", ephemeral=True)

def setup(ArisaInteraction):
    role(ArisaInteraction)
