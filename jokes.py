from __main__ import bot
import bs4
import urllib.request
import random

@bot.command()
async def Witz(ctx):
    parameter = ctx.message.content.split()[1:]
    if not parameter:
        return await ranjoke(ctx) 
    else:
        return await suchjoke(parameter, ctx)

async def ranjoke(ctx):
    html = urllib.request.urlopen("https://www.ajokeaday.com/jokes/random").read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    finden = soup.find(class_ = "jubilat")
    joke = finden.p.text.replace("<br>", "\n")
    await ctx.send(joke, tts=True)

async def suchjoke(parameter, ctx):
    url = f"https://www.ajokeaday.com/search?sortingType=All&filterType=winnerOnly&keywords={'+'.join(parameter)}&catId=&startdate=&enddate="
    html = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    finden = soup.find_all(class_ = "jubilat")
    joker = []
    for fund in finden:
        joker.append(fund.p.text.replace("<br>", "\n"))
    await ctx.send(random.choice(joker), tts=True) if joker else await ctx.send("Da gibts nichts!")