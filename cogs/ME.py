from discord.ext import commands
import embedMaker
import json
import asyncpg
import aiohttp

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
                                             'https://steamuserimages-a.akamaihd.net/ugc/785237978963961829'
                                             '/6FA7A17EA9C6211FC4DCC04D49EBDB908FFDA727/?imw=268&imh=268&ima=fit'
                                             '&impolicy=Letterbox&imcolor=%23000000&letterbox=true')
            await ctx.send(embed=me_embed.t)

    @me.command()
    async def map(self, ctx, description='Send a map of current trees with ME missions'):
        """Show a picture of all nations with mission trees"""
        await ctx.send('https://cdn.discordapp.com/attachments/439921164345802762/650748613747539968'
                       '/MissionsExpandedmissiontrees.png')

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
            if nation.lower() == 'rum':
                keyword = 'Rûm'
                print("reeceived Rum request.")
            else:
                keyword = nation.rstrip().replace(' ', '_')
            async with self.bot.db.acquire() as conn:
                tag = await conn.fetchval('SELECT tag FROM tags WHERE country=$1', nation)
                x = await conn.fetchrow('SELECT one, two, three, four, five, six, seven FROM idea_names WHERE tag=$1', tag)
        if tag is None:
            await ctx.send('Does your nation have Bielefeld as a name? Neko is sure it doesn\'t exist oAo')
            return
        if keyword in {'Angevin_Realm', 'Angevins'}:
            keyword = 'Angevin_Empire'
        if keyword in {'Sicily', 'The_Two_Sicilies'} or tag == 'TTS':
            keyword = 'Sicily_Two_Sicilies'
        if keyword == 'Roman_Empire':
            keyword = 'Rome'
        async with aiohttp.ClientSession() as cs:
            async with cs.head(f'http://modcoop.org/index.php?title=Expanded_Mod_Family/{keyword}') as r:
                if r.status == 200:
                    print("hey")
                    await ctx.send(f'We have missions for {nation}, which has the {tag} tag\nhttp://modcoop.org/index'
                                   f'.php?title=Expanded_Mod_Family/{keyword}')
                    print("too dumb to understand")
                    # sends idea expanded_data
                    y = ('Tradition', 'Ambition', *x)
                    counter = 0
                    me_body_message = '```'
                    print("that")
                    for key, value in vanillaDataIdeas[tag].items():
                        value = str(value).replace("'", "")
                        me_body_message = f'{me_body_message}{y[counter]}: {value.replace("{", "").replace("}", "")} \n'
                        counter += 1
                    me_body_message = me_body_message + '```'
                    print("or")
                    await ctx.send(me_body_message)
                    print("what")

                else:
                    await ctx.send('We haven\'t made missions for them!')
                    print(r.status)

    @me.command()
    async def formables(self, ctx):
        """Shows a list of all formable nations"""
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
