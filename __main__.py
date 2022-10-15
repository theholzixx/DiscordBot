from discord.ext import commands
import config
import discord
import asyncio

from Music.verwaltung import verwaltung

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

import hi, moin, helfer, zeit, ping, looper, jokes, music

@bot.event
async def on_ready():
    print(bot.latency)
    game = discord.Game("BOTOTOTOTOTOTOTOTOTOT")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Fertich")

bot.add_cog(verwaltung(bot))

bot.run(config.token)