from __main__ import bot
from enum import Flag
from discord.ext import commands
import asyncio
from time import sleep
import youtube_dl
import discord
import validators

global Waitlist
Waitlist = []
global admin
admin = False
global Globalctx
Globalctx = None

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '/Downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.command()
async def Nexts(ctx):
    Next(ctx)

def Next(ctx):
    print("next wurde auch aufgerufen")
    if len(Waitlist) == 0:
        print("No more songs in Waitlist.")
        #await Globalctx.send("No more songs in Waitlist.")        
    else:
        print("Next song.")
        #await Globalctx.send("Next song.")
        player = Waitlist[0]
        del Waitlist[0]
        #player = await YTDLSource.from_url(url, loop=bot.loop)
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        ctx.voice_client.play(player, after=lambda x= None: Next(ctx))

@bot.command()
async def Play(ctx):
    """Plays a Song(If YT URL is provided)"""
    # Gets voice channel of message author
    urlA = ctx.message.content.split(' ')

    if len(urlA) == 3:
        await ctx.send("nichtNow")
        url = urlA[2]
        admin = False
    elif len(urlA) == 4 and urlA[2] == "now":
        await ctx.send("NOW")
        url = urlA[3]
        if ctx.message.author.guild_permissions.administrator:
            admin = True
        else:
            admin = False
            await ctx.send("Not an admin.")
    else:
        url = None

    voice_channel = ctx.author.voice.channel
    if voice_channel != None:
        vc = ctx.voice_client
        if url != None:
            if not validators.url(url):
                await ctx.send("not a valid url")
            else:
                if admin or not ctx.voice_client.is_playing():
                    admin = False
                    async with ctx.typing():
                        player = await YTDLSource.from_url(url, loop=bot.loop)
                        if ctx.voice_client.is_playing():
                            vc.stop()
                        vc.play(player, after=lambda x=None: Next(ctx))
                        Globalctx = ctx
                    await ctx.send(f'Now playing: {player.title}')
                else:
                    #Add to Waitlist
                    Waitlist.append(await YTDLSource.from_url(url, loop=False))
                    await ctx.send("Song added to Waitlist.")

        else:
            vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg-2022-10-13-git-9e8a327e68-full_build/bin/ffmpeg.exe",
            source="C:/Users/hendr/Nextcloud/Musik/coole musik/Frozen Night - II- The Ethereal Forest/Frozen Night - II- The Ethereal Forest - 03 Chrysalis Metamorphosis.mp3"))
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.

def Test():
    print("Nix")

@bot.command()
async def Stop(ctx):
    """Stops and disconnects the bot from voice"""
    
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not connected to any voice channel on this server!")

@bot.command()
async def DelQ(ctx):
    #if ctx.author.voice.channel == ctx.voice_client:
        print(Waitlist)
        Waitlist = []
        print(Waitlist)
        await ctx.send("Waitlist deleted!")
    #else:
        #await ctx.send("Not in same Voicechannel!")

#@Next.before_invoke
#async def ensure_ctx(ctx):
#    Globalctx = ctx

@Play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    #elif ctx.voice_client.is_playing():
        #await ctx.send("Changing Song")