from __main__ import bot

@bot.command()
async def LOOP(ctx):
    await ctx.send("|say þLOOP", tts=True)