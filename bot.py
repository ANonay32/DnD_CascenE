
import nest_asyncio
nest_asyncio.apply()

import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
#import discord

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='&')

players = []
gmap = ""
gwidth = 0
gheight = 0

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def game_map(ctx, width: int, height: int):

    global gwidth
    global gheight
    global gmap

    gwidth = width*2 + 1
    gheight = height*2 + 1

    gmap = "";
    if width > height:
        temp = height
        height = width
        width = temp

    if ((width + 1) * height) > 1980:
        await ctx.channel.send("Given dimensions are too large, map area must be smaller than 1980 units")

    else:
        width = width*2
        for i in range(height):
            for j in range(width):
                if j == 0 or j == width - 1:
                    gmap += "|"
                elif i == 0:
                    gmap += "‾"
                elif i == height - 1:
                    gmap += "_"
                else:
                    gmap += " "
            gmap += "\n"
        await ctx.channel.send("```" + gmap + "```")

@bot.command()
async def build(ctx, tlx: int, tly: int, brx: int, bry: int):

    global gwidth
    global gheight
    global gmap

    chArray = list(gmap)

    for k in range(abs(tly - bry)):
        for l in range(abs(tlx - brx)*2):
            if l == 0 or l == abs(tlx - brx)*2 - 1:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = "|"
            elif k == abs(tly - bry) - 1:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = "_"
            elif k == 0:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = "‾"

            #await ctx.channel.send(str((tly + k)*gwidth) + " " + str(l) + " " + str(tlx))

    gmap = "".join(chArray)

    await ctx.channel.send("```" + gmap + "```")

@bot.command()
async def build_spec(ctx, tlx: int, tly: int, brx: int, bry: int, char: str):

    global gwidth
    global gheight
    global gmap

    chArray = list(gmap)

    for k in range(abs(tly - bry)):
        for l in range(abs(tlx - brx)*2):
            if l == 0 or l == abs(tlx - brx)*2 - 1:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = char
            elif k == abs(tly - bry) - 1:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = char
            elif k == 0:
                chArray[((tly + k)*gwidth + l + tlx*2 + 1)] = char

            #await ctx.channel.send(str((tly + k)*gwidth) + " " + str(l) + " " + str(tlx))

    gmap = "".join(chArray)

    await ctx.channel.send("```" + gmap + "```")

@bot.command()
async def add_player(ctx, name, xpos: int, ypos: int):
    global players
    global gmap
    global gwidth
    global gheight

    valid = True
    if xpos < 0 or xpos > gwidth - 1 or ypos < 0 or ypos > gheight - 1:
        await ctx.channel.send("Your character would be out of bounds at these coordinates")
        valid = False
    listMap = list(gmap)
    if listMap[ypos * gwidth + xpos] != " ":
        await ctx.channel.send("Your character would be inside a wall or something at these coordinates")
        valid = False
    if len(name) > 1:
        listMap[ypos * gwidth + xpos] = name[0]
    else:
        listMap[ypos * gwidth + xpos] = name
    if valid:
        players.append((name, xpos, ypos))
        gmap = "".join(listMap)
        await ctx.channel.send("```" + gmap + "```")

@bot.command()
async def repeat(ctx, arg):
	await ctx.channel.send(arg)

bot.run(TOKEN)
