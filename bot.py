# -*- coding: utf-8 -*-
<<<<<<< HEAD

=======
"""
Created on Sat Jan 16 22:26:21 2021

@author: lucas, Arthur, Noah, Klondike
"""
>>>>>>> dc4b8edf73eb58e7cbeeae07c7bfea1eaf6ad036


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

    if tlx>brx:
        temp = tlx
        tlx = brx
        brx = temp
        
    if tly>bry:
        temp = tly
        tly = bry
        bry = temp

    for k in range(abs(tly - bry)):
        for l in range(abs(tlx - brx)*2):
            if l == 0 or l == abs(tlx - brx)*2 - 1:
                chArray[((tly + k)*gwidth + l + tlx*2)] = "‖"
            elif k == abs(tly - bry) - 1:
                chArray[((tly + k)*gwidth + l + tlx*2)] = "‗"
            elif k == 0:
                chArray[((tly + k)*gwidth + l + tlx*2)] = "˭"

            #await ctx.channel.send(str((tly + k)*gwidth) + " " + str(l) + " " + str(tlx))

    gmap = "".join(chArray)

    await ctx.channel.send("```" + gmap + "```")
<<<<<<< Updated upstream

=======
    
    
>>>>>>> Stashed changes
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
async def save_as(ctx, filename: str):
	try:
		global gmap
		global gwidth
		global gheight
		f = open("_".join(["userFile",ctx.user,filename]), "w")
		f.write("\t".join([str(gwidth), str(gheight), gmap]))
		f.close()
		await ctx.channel.send("```File Written```")
	except Exception as e:
		await ctx.channel.send(f"```Error when writing file '{filename}' for user {ctx.user} with the following error:\n {str(e)}"[0:1996]+"```")

@bot.command()
async def load_map(ctx, filename: str):
	try:
		global gmap
		global gwidth
		global gheight
		f = open("_".join(["userFile",ctx.user,filename]), "r")
		temp = f.read()
		tgwidth, tgheight, gmap = temp.split("\t")
		gwidth = int(tgwidth)
		gheight = int(tgheight)
	except Exception as e:
		await ctx.channel.send(f"```Error when reading file '{filename}':\n {str(e)}"[0:1996]+"```")

@bot.command()
async def listplayers(ctx):
    for player in players:
        await ctx.channel.send(player[0])

@bot.command()
async def print(ctx, arg):
    await ctx.channel.send(arg)

@bot.command()
async def add_player(ctx, name, xpos: int, ypos: int):
    global players
    global gmap
    global gwidth
    global gheight

    xpos = xpos*2
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
async def move(ctx, name, newx: int, newy: int):
    
    newx = newx*2
    global gmap
    listMap = list(gmap)
    old = None
    
    valid = True
    if newx < 0 or newx > gwidth - 1 or newy < 0 or newy > gheight - 1:
        await ctx.channel.send("Your character would be out of bounds at these coordinates")
        valid = False
    if listMap[newy * gwidth + newx] != " ":
        await ctx.channel.send("Your character would be inside a wall or something at these coordinates")
        valid = False
        
    for player in players:
        if player[0] == name:
            old = player
           
        if old == None:
                await ctx.channel.send("This player does not exist. Check your spelling or use &players.")
                return
        
    listMap[old[2] * gwidth + old[1]] = " "
    if len(name) > 1:
        listMap[newy * gwidth + newx] = name[0]
    else:
        listMap[newy * gwidth + newx] = name
    if valid:
        players.append((name, newx, newy))
        gmap = "".join(listMap)
        await ctx.channel.send("```" + gmap + "```")
<<<<<<< HEAD
<<<<<<< HEAD
        
@bot.command()
async def line(ctx, x0: int, y0: int, x1: int, y1: int, char: str):
    
    global gwidth
    global gheight
    global gmap


    #start

    points = [];
    dx = x1 - x0
    dy = y1 - y0
    N =  max(abs(dx), abs(dy)*2);   #may move *2 to l in points loop
    
    for step in range(N+1):
        
        t = 0
        if (N == 0):
            t = 0.0
        else:
            t = step / N
        
        vx = round(x0 + t * dx)
        vy = round(y0 + t * dy)
        
        pxy = (vx, vy)
        
        points.append(pxy)
        

    chArray = list(gmap)
    
    
    for pr in points:
        chArray[(pr[1]*gwidth + pr[0]*2 + 1)] = char
    
    gmap = "".join(chArray)
    
    await ctx.channel.send("```" + gmap + "```")


<<<<<<< Updated upstream
=======


@bot.command()
async def line(ctx, x0: int, y0: int, x1: int, y1: int, char: str):
    
    global gwidth
    global gheight
    global gmap
    

    #start

    points = [];
    dx = x1 - x0
    dy = y1 - y0
    N =  max(abs(dx), abs(dy));
    
    for step in range(N+1):
        
        t = 0
        if (N == 0):
            t = 0.0
        else:
            t = step / N
        
        vx = round(x0 + t * dx)
        vy = round(y0 + t * dy)
        
        points.append(vx)
        points.append(vy)
        

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


>>>>>>> Stashed changes
@bot.command()
async def repeat(ctx, arg):
	await ctx.channel.send(arg)

=======

@bot.command()
async def repeat(ctx, arg):
	await ctx.channel.send(arg)
bot.run(TOKEN)
>>>>>>> dc4b8edf73eb58e7cbeeae07c7bfea1eaf6ad036
