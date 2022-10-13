from __main__ import bot
from time import sleep
import youtube_dl
import discord

#@bot.command()
#async def Play(ctx):
#    await ctx.send("Neeeeee")

@bot.command()
async def Play(ctx):
    # Gets voice channel of message author
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel != None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg-2022-10-13-git-9e8a327e68-full_build/bin/ffmpeg.exe", source="C:/Users/hendr/Nextcloud/Musik/Dj Schwede - Ihre Bestellung bitte.mp3"))
        #await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.

@bot.command()
async def Stop(ctx):
    vc = ctx.author.voice.channel
    await vc.disconnect()