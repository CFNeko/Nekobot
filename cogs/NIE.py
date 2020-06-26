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


class NIE(commands.Cog):
    """National Ideas Expanded"""
    def __init__(self, bot):
        self.bot = bot
    @commands.group(case_insensitive=True)
    async def nie(self, ctx):
        """Returns the NIE steam page"""
        if ctx.invoked_subcommand is None:
            nieEmbed = embedMaker.embedMaker('National Ideas Expanded', 'https://steamcommunity.com/sharedfiles/filedetails/?id=1592328478', 'I have an idea!', 0xd5000, 'Made by Verinity', 'https://steamuserimages-a.akamaihd.net/ugc/1183831643854233426/87693DEED6CA2C98B9CA088B36C272B030572FEF/?imw=268&imh=268&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true')
            await ctx.send(embed=nieEmbed.t)
    @nie.command()
    async def find(self, ctx, *, country: str):
        """!nie find [tag] Sends back the nation with NIE ideas"""
        if len(country) != 3:
            async with self.bot.db.acquire() as conn:
                print(f'NIE full name request received: {country}')
                country = await conn.fetch('SELECT tag FROM tags WHERE country=$1'. country)
            print(f'NIE request adapted to: {country}')
        try:
            print(f'NIE request received {country}')
            nieBodyMessage = f'```{nieDataDescription[country]} \n----------\n'
            for key, value in nieData[country].items():
                nieBodyMessage = nieBodyMessage + f'{key.title()}: {value} \n'
            nieBodyMessage = nieBodyMessage + '```'
            await ctx.send(nieBodyMessage)
        except:
            await ctx.send('Neko couldn\'t find it T~T')
    @nie.command()
    async def formables(self, ctx):
        """Shows a list of all formable nations"""
        async with self.bot.db.acquire() as conn:
            message = '```'
            me_data = await conn.fetch('SELECT (tag, country) FROM tags WHERE nie_tag')
            for info in me_data:
                for data in info:
                    message = message + f'{str(data[0])} : {str(data[1])} \n'
            message = message + '```'
            await ctx.send(message)

def setup(bot):
    bot.add_cog(NIE(bot))
