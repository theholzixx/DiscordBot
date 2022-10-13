from discord.ext import commands
from Music import join, play

class verwaltung(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.command()
    async def Join(self, ctx):
        await join.join2(ctx)

    @commands.command()
    async def Play(self, ctx, url):
        await play.play2(ctx, url, self.bot)

    @commands.command()
    async def Stop(self, ctx):
        await ctx.voice_client.disconnect()

    @Play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()