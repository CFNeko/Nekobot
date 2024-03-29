import discord
from discord.ext import commands
import embedMaker
import json
import asyncpg

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
        """+nie find [tag] Sends back the nation with NIE ideas"""
        x = country
        if len(country) == 3 and x.isupper():
            print(f'NIE tag request received: {x}')
            async with self.bot.db.acquire() as conn:
                country = await conn.fetchval('SELECT country FROM tags WHERE tag=$1', x)
                tag = x
        else:
            print(f'NIE country request received: {country}') 
            async with self.bot.db.acquire() as conn:
                tag = await conn.fetchval('SELECT tag FROM tags WHERE country=$1', x)
        try:
            nieBodyMessage = f'```{nieDataDescription[tag]} \n----------\n'
            for key, values in nieData[country].items():
                nieBodyMessage = nieBodyMessage + f'{key.title()}: {values} \n'
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

    @nie.command()
    async def countries(self, ctx):
        """Shows a list of all nations with NIE ideas"""
        await ctx.send('Here\'s a list of all NIE coubtries: https://pastebin.com/XTu65Rdn')

def setup(bot):
    bot.add_cog(NIE(bot))
