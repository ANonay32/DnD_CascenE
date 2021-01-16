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

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild: \n'
        f'{guild.name}(id: {guild.id})'
        )

@bot.command()
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def game_map(ctx):
	await ctx.channel.send("```|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|\n|                                |\n|                                |\n|                                |\n|--------------------------------|```")

bot.run(TOKEN)
