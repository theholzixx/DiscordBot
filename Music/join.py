import discord

async def join2(ctx):
    channel = ctx.message.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

    await channel.connect()
    await ctx.send("Verbunden!")