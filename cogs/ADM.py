from discord.ext import commands
import embedMaker
import json
import asyncpg
import aiohttp
import os

BOT_ADMIN_SERVER = os.getenv('BOT_ADMIN_SERVER')
BOT_ADMIN_CHAN = os.getenv('BOT_ADMIN_CHAN')


def _is_admin(ctx):
    return ctx.author.guild.name == BOT_ADMIN_SERVER and ctx.channel.name == BOT_ADMIN_CHAN


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
    async def me_add(self, ctx, *, args: str):
        """add a mission entry, but ONLY if you're admin"""
        async with self.bot.db.acquire() as conn:
            if _is_admin(ctx):
                params_array = args.split(" ")
                tag = params_array[0]
                is_me = params_array[-1]
                name = " ".join(params_array[1:-1])
                await ctx.send(f"the tag is {tag}, the name is {name} and is_me is {is_me}")
            else:
                await ctx.send("GET OUT, peasant! (but nice try)")

    @adm.command()
    async def me_suppress(self, ctx):
        """suppress a mission entry, but ONLY if you're admin"""
        async with self.bot.db.acquire() as conn:
            if _is_admin(ctx):
                await ctx.send("hey, you're admin, amirite")
            else:
                await ctx.send("GET OUT, peasant! (but nice try)")


def setup(bot):
    bot.add_cog(ADM(bot))
