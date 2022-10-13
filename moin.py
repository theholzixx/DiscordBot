from __main__ import bot
import time

@bot.command()
async def Moin(ctx):
    milli_sec = int(round(time.time() * 1000))
    if milli_sec % 2:
        await ctx.send("Wa?\nMoin.", tts=True)
    else:
        await ctx.send("---")