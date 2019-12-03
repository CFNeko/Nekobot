import discord
from discord.ext import commands
import random
import asyncpg

class commands(commands.Cog):
    "A list of all non-mod commands"
    def __init__(self, bot):
        self.bot = bot
    @commands.command(case_insensitive=True)
    async def jay(self, ctx):
        """Praises Jay"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Praisu Jayu')
    @commands.command(case_insensitive=True)
    async def boss(self, ctx):
        """Questions Boss"""
        if ctx.invoked_subcommand is None:
            await ctx.send('The know-it-all-retard')
    @commands.command(case_insensitive=True)
    async def neko(self, ctx):
        """Drinks Coffee"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Neko prefers tea but oh well:')
            await ctx.send('https://ko-fi.com/B0B812IOW')
    @commands.command(case_insensitive=True)
    async def members(self, ctx):
        """Returns a list of members in the server"""
        totalMembers = len(set(ctx.bot.get_all_members()))
        await ctx.send(f'Our server has {totalMembers} professional map watchers!')
    @commands.command(case_insensitive=True)
    async def help(self, ctx, *cog):
        """You're using this command :0"""
        if len(cog) < 1:
            halp=discord.Embed(title='All commands for Neko Neko', description='Use `+help [command]` to get further details')
            cogs_desc = ''
            for x in self.bot.cogs:
                if x == 'Events': continue
                cogs_desc += (f'{x.title()} - {self.bot.cogs[x].__doc__}\n')
            halp.add_field(name='Commands',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
            await ctx.send(embed=halp)
        else:
            found = False
            for x in self.bot.cogs:
                for y in cog:
                    if x == y:
                        halp=discord.Embed(title='Command List for +'+cog[0].upper(),description=self.bot.cogs[cog[0]].__doc__)
                        for c in self.bot.get_cog(y).walk_commands():
                            if not c.hidden:
                                halp.add_field(name='+'+c.name.title(),value=c.help,inline=False)
                            found = True
            if not found: await ctx.message.author.send('Does that command exist~? O_o')
            else: await ctx.send(embed=halp)
    @commands.command(case_insensitive=True)
    async def tag(self, ctx, *, nation:str):
        nation.title()
        conn = await asyncpg.connect('postgresql://postgres@localhost/expanded_data')
        tag = await conn.fetchval('SELECT tag FROM tags WHERE country=$1', nation)
        await ctx.send(str(tag))

   


def setup(bot):
    bot.add_cog(commands(bot))
