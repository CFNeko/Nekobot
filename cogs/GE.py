import discord
from discord.ext import commands
import embedMaker
import requests


class ge(commands.Cog):
    """Governments Expanded"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)
    async def ge(self, ctx):
        """Returns the GE steam page"""
        if ctx.invoked_subcommand is None:
            geEmbed = embedMaker.embedMaker('Governments Expanded', 'https://steamcommunity.com/sharedfiles/filedetails/?id=1596815683', 'The best part of Dharma', 0x531b93, 'Made by Jay', 'https://steamuserimages-a.akamaihd.net/ugc/794243175441321379/94E146928B3CA6CEA4A8762F72F3633DF8E9569D/')
            await ctx.send(embed=geEmbed.t)

    @ge.command()
    async def info(self, ctx):
        """Gives a spreadsheet of all GE reforms"""
        await ctx.send('https://docs.google.com/spreadsheets/d/1XMmAGpxIdBXCLpffkNvzkXvluiLcZwVBYUozJ_96sQs/edit#gid=2115281575')

    @ge.command()
    async def empowered(self, ctx):
        """Explains what are empowered reforms"""
        await ctx.send('Empowered reforms work similarly to rpg skill trees. Early generic reforms are available to all nations, but your choice will accrue you points in the following categories: clergy/burghers/nobility/royalty.  After Tier 3, the combination of these points unlock not only hidden reforms, but stronger ones too.')

    @ge.command()
    async def patreon(self, ctx):
        gepEmbed = embedMaker.embedMaker('Governments Expanded Patreon', 'https://www.patreon.com/user?u=16752311', 'Support the developer!', 0x531b93, 'Made by Jay', 'https://aescifi.ca/wp/wp-content/uploads/2019/05/Patreon-Icon.png')
        await ctx.send(embed=gepEmbed.t)


def setup(bot):
    bot.add_cog(ge(bot))
