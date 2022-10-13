from __main__ import bot

@bot.command()
async def Help(ctx):
    await ctx.send("""þMoin 'Reagiert manchmal
þHi 'Sagt ganz nett Hallo.
þWie_spät 'Sagt wie spät es ist.
þPing 'Pong
þWitz [suchwort1 suchwort2...] 'Ohne Suchwort: Random witz. Mit Suchwort: Witz passend zu den Suchwörtern.
þJoin 'Hört dir zu. Sagt aber nix.
þPlay [yt url] 'Spielt dein Yt video ab.
þHelp 'Sie sind hier!""")