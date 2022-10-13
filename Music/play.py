from Music.musicholen import YTDLSource
import os
    
async def play2(ctx, url, bot):
    """Plays from a url (almost anything youtube_dl supports)"""

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        ctx.voice_client.play(player, after=aufräumen)

    await ctx.send('Now playing: {}'.format(player.title))

def aufräumen(error):

    root = r"C:/Users/hendr/Nextcloud/Programmier Stuff/Python/Discord_Bot"

    if error:
        print('Player error: %s')# % e)
    
    datein = os.listdir(root)

    for datei in datein:
        if datei.startswith("youtube"):
            print(f"Die datei {datei} wurde gelöscht.")
            os.remove(os.path.join(root, datei))