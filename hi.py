from __main__ import bot

@bot.command()
async def Hi(ctx):
    await ctx.send("MOIN MOIN DU SACKFALTE!", tts=True)