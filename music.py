from __main__ import bot
from enum import Flag
from socket import SO_LINGER
from discord.ext import commands
import asyncio
import youtube_dl
import discord
import validators

global Waitlist
Waitlist = []
global admin
admin = False
global Song
Song = None
global More
More = False

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
async def Next(ctx):
    """Plays the Next song in Queue"""

    global More
    print("Nextsong command")
    Next_song(ctx)
    if not More:
        await ctx.send("No more songs in Waitlist.")

def Next_S(ctx):
    loop = asyncio.get_running_loop()
    loop.create_task(Next_song(ctx))

def Next_song(ctx):
    global Song
    global Waitlist
    global More
    print("next wurde auch aufgerufen")
    if len(Waitlist) == 0:
        More = False
        print("No more songs in Waitlist.")
        if Song is not None:
            Song.title = "No Song Playing"
    else:
        More = True
        print("Next song.")
        player = Waitlist[0]
        del Waitlist[0]
        ctx.voice_client.play(player, after=lambda x=None: Next_song(ctx))
        Song = player

@bot.command()
async def Play(ctx):
    """Plays a Song(If YT URL is provided)"""

    global Waitlist
    urlA = ctx.message.content.split(' ')

    if len(urlA) == 3:
        url = urlA[2]
        admin = False
    elif len(urlA) == 4 and urlA[2] == "now":
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
                        vc.play(player, after=lambda x=None: Next_song(ctx))
                        global Song 
                        Song = player
                    await ctx.send(f'Now playing: {player.title}')
                else:
                    #Add to Waitlist
                    async with ctx.typing():
                        Waitlist.append(await YTDLSource.from_url(url, loop=False))
                    await ctx.send("Song added to Waitlist.")

        else:
            await ctx.send("Please provide a url.")
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.

@bot.command()
async def Info(ctx):
    """Showes Title of current Song"""

    await ctx.send(f'Now playing: {Song.title}')

@bot.command()
async def Stop(ctx):
    """Stops and disconnects the bot from voice"""
    
    if ctx.voice_client is not None and ctx.author.voice.channel.id == ctx.voice_client.channel.id:
        await ctx.voice_client.disconnect()
        await DelQ(ctx)
    elif ctx.author.voice.channel.id != ctx.voice_client.channel.id:
        await ctx.send("Not in same Voicechannel!")
    else:
        await ctx.send("I am not connected to any voice channel on this server!")

@bot.command()
async def Queue(ctx):
    """All Songs in current Queue"""

    if len(Waitlist) != 0:
        Titel = "Current Queue: \n"
        for x in range(len(Waitlist)):
            Titel += str(x + 1) + ": " + Waitlist[x].title + "\n"
            print(x)
        await ctx.send(Titel)
    else:
        await ctx.send("No Title in Queue.")

@bot.command()
async def DelQ(ctx):
    """Delete all Songs from Queue"""

    global Waitlist
    if ctx.voice_client is None or ctx.author.voice.channel.id == ctx.voice_client.channel.id:
        print(Waitlist)
        Waitlist = []
        print(Waitlist)
        await ctx.send("Waitlist deleted!")
    else:
        await ctx.send("Not in same Voicechannel!")

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