import discord
from discord.ext import commands
import asyncpg


class Commands(commands.Cog):
    """A list of all non-mod commands"""
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
        print("Sending member count")
        total_members = ctx.guild.member_count
        await ctx.send(f'Our server has {total_members} professional map watchers!')


    @commands.command(case_insensitive=True)
    async def help(self, ctx, *cog):
        """You're using this command :0"""
        if len(cog) < 1:
            help_message = discord.Embed(title='All commands for Neko Neko', description='Use `+help [command]` to '
                                                                                         'get further details')
            cogs_desc = ''
            for x in self.bot.cogs:
                if x == 'Events':
                    continue
                cogs_desc += f'{x.title()} - {self.bot.cogs[x].__doc__}\n'
            help_message.add_field(name='Commands', value=cogs_desc[0:len(cogs_desc)-1], inline=False)
            await ctx.send(embed=help_message)
        else:
            found = False
            for x in self.bot.cogs:
                for y in cog:
                    if x.lower() == y.lower():
                        # TODO formalise probably with a real dict the link between cogs and this place (because the
                        #  upper everywhere will some day explode in our face...)
                        help_message = discord.Embed(title='Command List for +'+cog[0].upper(),
                                                     description=self.bot.cogs[cog[0].upper()].__doc__)
                        for c in self.bot.get_cog(y.upper()).walk_commands():
                            if not c.hidden:
                                help_message.add_field(name='+'+c.name.title(), value=c.help, inline=False)
                            found = True
            if not found:
                await ctx.message.author.send('Does that command exist~? O_o')
            else:
                await ctx.send(embed=help_message)

    @commands.command(case_insensitive=True)
    async def tag(self, ctx, *, nation: str):
        nation.title()
        async with self.bot.db.acquire() as conn:
            tag = await conn.fetchval('SELECT tag FROM tags WHERE country=$1', nation)
            await ctx.send(str(tag))


def setup(bot):
    bot.add_cog(Commands(bot))
