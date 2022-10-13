from __main__ import bot
import datetime

@bot.command()
async def Wie_spät(ctx):
    Uhr = datetime.datetime.now()
    await ctx.send(Uhr.strftime("Es ist %H:%M:%S"), tts=True)