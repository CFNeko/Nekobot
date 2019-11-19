import discord
from discord.ext import commands
import embedMaker
import json

with open('./expandedData/NIE_country_ideas.json', 'r') as f:
    fhand = f.read()
    nieData = json.loads(fhand)
with open('./expandedData/NIE_descriptions.json', 'r') as f:
    fhand = f.read()
    nieDataDescription = json.loads(fhand)

class nie(commands.Cog):
    """National Ideas Expanded"""
    def __init__(self, bot):
        self.bot = bot
    @commands.group(case_insensitive=True)
    async def nie(self, ctx):
        """Returns the NIE steam page"""
        if ctx.invoked_subcommand is None:
            nieEmbed = embedMaker.embedMaker('National Ideas Expanded', 'https://steamcommunity.com/sharedfiles/filedetails/?id=1592328478', 'I have an idea!', 0xd5000, 'Made by Verinity', 'https://steamuserimages-a.akamaihd.net/ugc/788614596622808953/47EA4EC5540814CA95971F4CAF6480960B200D0B/')
            await ctx.send(embed=nieEmbed.t)
    @nie.command()
    async def find(self, ctx, *, country: str):
        """!nie find [tag] Sends back the nation with NIE ideas"""
        country = country.upper()
        try:
            print(f'NIE request received {country}')
            nieBodyMessage = f'```{nieDataDescription[country]} \n----------\n'
            for key, value in nieData[country].items():
                nieBodyMessage = nieBodyMessage + f'{key.title()}: {value} \n'
            nieBodyMessage = nieBodyMessage + '```'
            await ctx.send(nieBodyMessage)
        except:
            await ctx.send('Neko couldn\'t find it T~T')


def setup(bot):
    bot.add_cog(nie(bot))
