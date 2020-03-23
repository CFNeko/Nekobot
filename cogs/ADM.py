from discord.ext import commands
import embedMaker
import json
import asyncpg
import aiohttp
import os

BOT_ADMIN_SERVER = os.getenv('BOT_ADMIN_SERVER')
BOT_ADMIN_CHAN = os.getenv('BOT_ADMIN_CHAN')


class ADM(commands.Cog):
    """Missions Expanded"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)
    async def adm(self, ctx):
        """Returns the ME steam page"""
        if ctx.invoked_subcommand is None:
            me_embed = embedMaker.embedMaker('admin the bot', 'https://steamcommunity.com/sharedfiles/filedetails'
                                                                  '/?id=1349005102', 'Missions to feed your '
                                                                                     'families', 0x00fdff,
                                             'VERY restricted',
                                             'https://steamuserimages-a.akamaihd.net/ugc/785237978963961829'
                                             '/6FA7A17EA9C6211FC4DCC04D49EBDB908FFDA727/?imw=268&imh=268&ima=fit'
                                             '&impolicy=Letterbox&imcolor=%23000000&letterbox=true')
            await ctx.send(embed=me_embed.t)

    @adm.command()
    async def test(self, ctx):
        """should work ONLY if you're admin"""
        async with self.bot.db.acquire() as conn:
            if ctx.author.guild.name == BOT_ADMIN_SERVER and ctx.channel.name == BOT_ADMIN_CHAN:
                await ctx.send("hey, you're admin, amirite")
            else:
                await ctx.send("GET OUT, peasant! (but nice try)")


def setup(bot):
    bot.add_cog(ADM(bot))
