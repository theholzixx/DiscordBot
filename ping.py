from __main__ import bot

@bot.command()
async def Ping(ctx):
    pinger = bot.latency * 1000
    await ctx.send(f"Pong {pinger:.1f} ms!")