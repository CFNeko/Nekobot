from discord.ext import commands
import embedMaker
import json
import asyncpg
import aiohttp
from bs4 import BeautifulSoup

with open('./vanillaData/countryIdeas.json', 'r') as f:
    fhand = f.read()
    vanillaDataIdeas = json.loads(fhand)

 
class ME(commands.Cog):
    """Missions Expanded"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)
    async def me(self, ctx):
        """Returns the ME steam page"""
        if ctx.invoked_subcommand is None:
            me_embed = embedMaker.embedMaker('Missions Expanded', 'https://steamcommunity.com/sharedfiles/filedetails'
                                                                  '/?id=1349005102', 'Missions to feed your '
                                                                                     'families', 0x00fdff,
                                             'Made by The Senate',
                                             'https://steamuserimages-a.akamaihd.net/ugc/786379195095939192/511DEC82C361BEBCE5C5C8ED5068C4915EEF4290/?imw=268&imh=268&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true'
                                             '/6FA7A17EA9C6211FC4DCC04D49EBDB908FFDA727/?imw=268&imh=268&ima=fit'
                                             '&impolicy=Letterbox&imcolor=%23000000&letterbox=true')
            await ctx.send(embed=me_embed.t)

    @me.command()
    async def map(self, ctx, description='Send a map of current trees with ME missions'):
        """Show a picture of all nations with mission trees"""
        await ctx.send('https://i.redd.it/6rgxxxpi83k41.png')

    @me.command()
    async def find(self, ctx, *, nation: str):
        """Searches for a country and sees if it has missions (+me find Golden Horde)"""
        if len(nation) == 3 and nation.isupper():
            tag = nation
            print(f'Wiki request received! {tag}')
            async with self.bot.db.acquire() as conn:
                keyword = await conn.fetchval('SELECT country FROM tags WHERE tag=$1', tag)
                nation = keyword
                keyword = nation.rstrip().replace(' ', '_')
                x = await conn.fetchrow('SELECT one, two, three, four, five, six, seven FROM idea_names WHERE tag=$1', tag)
        else:
            nation = nation.title()
            print(f'Wiki request received! {nation}')
            async with self.bot.db.acquire() as conn:
                tag = await conn.fetchval('SELECT tag FROM tags WHERE country=$1', nation)
                x = await conn.fetchrow('SELECT one, two, three, four, five, six, seven FROM idea_names WHERE tag=$1', tag)
        if tag is None:
            await ctx.send('Does your nation have Bielefeld as a name? Neko is sure it doesn\'t exist oAo')
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://sites.google.com/view/missions-expanded-trees/index') as r:
                await ctx.send(f'We have missions for {nation}, which has the {tag} tag')
                tree = await r.read()
                soup = BeautifulSoup(tree, 'html.parser')
                for link in soup.find_all('a', href=True):
                    if nation in link:
                        result = 'https://sites.google.com' + link['href']
                await ctx.send(result)
                # sends idea expanded_data
                # y = ('Tradition', 'Ambition', *x)
                # counter = 0
                # me_body_message = '```'
                # for key, value in vanillaDataIdeas[tag].items():
                #     value = str(value).replace("'", "")
                #     me_body_message = f'{me_body_message}{y[counter]}: {value.replace("{", "").replace("}", "")} \n'
                #     counter += 1
                # me_body_message = me_body_message + '```'

    @me.command()
    async def formables(self, ctx):
        """Shows a list of all formable nations in ME"""
        async with self.bot.db.acquire() as conn:
            message = '```'
            me_data = await conn.fetch('SELECT (tag, country) FROM tags WHERE me_tag')
            for info in me_data:
                for data in info:
                    message = message + f'{str(data[0])} : {str(data[1])} \n'
            message = message + '```'
            await ctx.send(message)


def setup(bot):
    bot.add_cog(ME(bot))
