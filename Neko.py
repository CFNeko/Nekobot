import discord
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
import sys, traceback
import embedMaker
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')


# load cogs
bot = commands.Bot(command_prefix='+', description='A Neko Neko Bot', case_insensitive=True)
bot.remove_command('help')
startup_extensions = ['cogs.ME', 'cogs.GE', 'cogs.SE', 'cogs.NIE', 'cogs.TGE', 'cogs.WU', 'cogs.Commands', 'cogs.Events', 'cogs.MCE']
for ext in startup_extensions:
    try:
        bot.load_extension(ext)
    except Exception as e:
        print(f'Something went wrong when tried to load extension {ext}: {e}')


async def run():
    credentials = {"user": DB_USER, "password": DB_PASSWORD, "database": DB_NAME, "host": DB_HOST}
    db = await asyncpg.create_pool(**credentials)
    bot.db = db


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
print('Neko Neko Nii~')
bot.run(DISCORD_TOKEN, reconnect=True)
