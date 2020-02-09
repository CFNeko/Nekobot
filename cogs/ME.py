import discord
from discord.ext import commands
import embedMaker
import requests
import json
import asyncpg
import aiohttp

with open('./vanillaData/countryIdeas.json', 'r') as f:
    fhand = f.read()
    vanillaDataIdeas = json.loads(fhand)


class me(commands.Cog):
    """Missions Expanded"""
    def __init__(self, bot):
        self.bot = bot
    @commands.group(case_insensitive=True)
    async def me(self, ctx):
        "Returns the ME steam page"
        if ctx.invoked_subcommand is None:
            meEmbed = embedMaker.embedMaker('Missions Expanded', 'https://steamcommunity.com/sharedfiles/filedetails/?id=1349005102', 'Missions to feed your families', 0x00fdff, 'Made by The Senate', 'https://steamuserimages-a.akamaihd.net/ugc/785237978963961829/6FA7A17EA9C6211FC4DCC04D49EBDB908FFDA727/?imw=268&imh=268&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true')
            await ctx.send(embed=meEmbed.t)
    @me.command()
    async def map(self, ctx, description='Send a map of current trees with ME missions'):
        "Show a picture of all nations with mission trees"
        await ctx.send('https://cdn.discordapp.com/attachments/439921164345802762/650748613747539968/MissionsExpandedmissiontrees.png')
    @me.command()
    async def find(self, ctx, *, nation: str):
        """Searches for a country and sees if it has missions (+me find Golden Horde)"""
        if len(nation) == 3 and nation.isupper():
            tag = nation
            print(f'Wiki request received! {tag}')
            async with self.bot.db.acquire() as conn:
                keyWord = await conn.fetchval('SELECT country FROM tags WHERE tag=$1', tag)
                nation = keyWord
                keyWord = nation.rstrip().replace(' ', '_')
                x = await conn.fetchrow('SELECT one, two, three, four, five, six, seven FROM idea_names WHERE tag=$1', tag)
        else:
            nation = nation.title()
            print(f'Wiki request received! {nation}')
            if nation.lower() = 'rum':
                keyWord = 'Rûm',
            else:
                keyWord = nation.rstrip().replace(' ', '_')
            async with self.bot.db.acquire() as conn:
                tag = await conn.fetchval('SELECT tag FROM tags WHERE country=$1', nation)
                x = await conn.fetchrow('SELECT one, two, three, four, five, six, seven FROM idea_names WHERE tag=$1', tag)
        if tag is None:
            await ctx.send('Does your nation have Bielefeld as a name? Neko is sure it doesn\'t exist oAo')
            return
        if keyWord in {'Angevin_Realm', 'Angevins'}: keyWord = 'Angevin_Empire'
        if keyWord in {'Sicily','The_Two_Sicilies'} or tag == 'TTS' : keyWord = 'Sicily_Two_Sicilies'
        if keyWord == 'Roman_Empire': keyWord = 'Rome'
        async with aiohttp.ClientSession() as cs:
            async with cs.head(f'http://modcoop.org/index.php?title=Expanded_Mod_Family/{keyWord}') as r:
                if r.status == 200:
                    await ctx.send(f'We have missions for {nation}, which has the {tag} tag\nhttp://modcoop.org/index.php?title=Expanded_Mod_Family/{keyWord}')
                    #sends idea expanded_data
                    y = ('Tradition', 'Ambition', *x)
                    counter = 0
                    meBodyMessage = '```'
                    for key, value in vanillaDataIdeas[tag].items():
                        value = str(value).replace("'", "")
                        meBodyMessage =  meBodyMessage + f'{y[counter]}: {value.replace("{", "").replace("}", "")} \n'
                        counter += 1
                    meBodyMessage =  meBodyMessage + '```'
                    await ctx.send(meBodyMessage)

                else:
                    await ctx.send('We haven\'t made missions for them!')

    @me.command()
    async def formables(self,ctx):
        "Shows a list of all formable nations"
        async with self.bot.db.acquire() as conn:
            conn = await asyncpg.connect('postgresql://postgres@localhost/expanded_data')
            message = '```'
            meData = await conn.fetch('SELECT (tag, country) FROM tags WHERE me_tag')
            for info in meData:
                for data in info:
                    message = message + f'{str(data[0])} : {str(data[1])} \n'
            message = message + '```'
            await ctx.send(message)


def setup(bot):
    bot.add_cog(me(bot))
