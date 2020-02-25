import discord
from discord.ext import commands
import embedMaker
import json
import aiohttp
from bs4 import BeautifulSoup

lhand = open('./vanillaData/loc.txt')
with open('./vanillaData/Backup0.json', 'r') as f:
    fhand = f.read()
    data = json.loads(fhand)
with open('./debugging_tools/Backup0.txt.json', 'r') as f:
    fhand = f.read()
    data2 = json.loads(fhand)


class WU(commands.Cog):
    """Waifu Universalis"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)
    async def wu(self, ctx):
        """Returns the WU steam page"""
        if ctx.invoked_subcommand is None:
            wuEmbed = embedMaker.embedMaker('Waifu Universalis',
                                            'https://steamcommunity.com/sharedfiles/filedetails/?id=1326039079',
                                            'EU4 but anime', 0xE59400, 'Made by claivin',
                                            'https://cdn.discordapp.com/attachments/422851447936516116/570523904632684547/VEN.png')
            await ctx.send(embed=wuEmbed.t)

    @wu.command()
    async def find(self, ctx, *, waifu: str):
        """Searches for your dream waifu"""
        waifu = waifu.replace(' ', '-')
        async with self.bot.db.acquire() as conn:
            result = await conn.fetchval('SELECT (code) FROM wu_waifuts WHERE waifu = $1', waifu.title())
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    f'https://www.deviantart.com/c-----n/art/{waifu}-Universalis-Mod-Asset--{str(result)}') as r:
                text = await r.read()
                x = BeautifulSoup(text.decode('utf-8'), 'html.parser')
                mydivs = x.findAll("img", {"class": "_1izoQ"})
                embed = discord.Embed()
                embed.set_image(url=mydivs[0]['src'])
                await ctx.send(embed=embed)
            # await ctx.send('Neko can\'t find your waifu, maybe it doesn\'t exist?')

        # for line in lhand:
        #     print('YES')
        #     #line.split(',')
        #     x = line.find(',')
        #     var = line[:x].strip()
        #     word = line[x+1:].strip()
        #     await conn.execute('UPDATE idea_names SET one = $1 WHERE one =$2', word, var)
        #     await conn.execute('UPDATE idea_names SET two = $1 WHERE two =$2', word, var)
        #     await conn.execute('UPDATE idea_names SET three = $1 WHERE three =$2', word, var)
        #     await conn.execute('UPDATE idea_names SET four = $1 WHERE four =$2', word, var)
        #     await conn.execute('UPDATE idea_names SET five = $1 WHERE five =$2', word, var)
        #     await conn.execute('UPDATE idea_names SET six = $1 WHERE six =$2', word, var)
        #     await conn.execute('UPDATE idea_names SET seven = $1 WHERE seven =$2', word, var)
        # counter = 1
        # repeated = False
        # conn = await asyncpg.connect('postgresql://postgres@localhost/expanded_data')
        # await conn.execute('''DELETE FROM idea_names;
        # ALTER SEQUENCE idea_names_id_seq RESTART WITH 1;
        # ''')
        # for x, y in data.items():
        #     z = list(y.keys())
        #     z[0] = y['trigger']['tag']
        #     if type(z[0]) is list:
        #         print(f'found repetition in {counter} line')
        #         for x in y['trigger']['tag']:
        #             await conn.execute('''INSERT INTO idea_names (tag, one, two, three, four, five, six, seven, id) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)''', x, z[1], z[2], z[3], z[4], z[5], z[6], z[7], counter)
        #             counter += 1
        #     else:
        #         await conn.execute('''INSERT INTO idea_names (tag, one, two, three, four, five, six, seven, id) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)''', z[0], z[1], z[2], z[3], z[4], z[5], z[6], z[7], counter)
        #     counter += 1


class DVE(commands.Cog):
    """Development Expanded"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def dve(self, ctx):
        """Returns the DVE steam page"""
        if ctx.invoked_subcommand is None:
            dveEmbed = embedMaker.embedMaker('Development Expanded',
                                             'https://steamcommunity.com/sharedfiles/filedetails/?id=1880075247',
                                             'The best part of Common sense', 0x531b93, 'Made by Jay',
                                             'https://media.discordapp.net/attachments/613311500039225364/627719980041109514/13Artboard_1.png')
            await ctx.send(embed=dveEmbed.t)

    @dve.command()
    async def info(self, ctx):
        """Gives general info about DVE"""
        await ctx.send('''Three core rules
                        \nA. Provinces grow quickly up to a local development cost 55.
                        \nB. Afterwards, provinces grow slowly through prosperity and the lower your development cost is.
                        \nC. Province development goes down through devastation and warfare.
                        ''')

    @dve.command()
    async def modes(self, ctx):
        """DVE modes and how it works"""
        await ctx.send('''
                        \nNormal mode: normal growth and decay.
                        \nRealism mode: normal growth, insanely destructive decay.
                        \nMadness mode: where all growth and decline is modified to madness, and people breed and die at an incredible rate, Amazing for multiplayer where you can burn a country to the ground in a year or two, yet its good as new a decade later.
                        ''')

    @dve.command()
    async def genocide(self, ctx):
        """DVE culture spread and genocide"""
        await ctx.send('''
                        \nNone: why.
                        \nClassic: when devastated, countries will adopt the culture of neighboring provinces.
                        \nGenocidal: insanely fast culture change, easily wiping out entire culture group from the map
                        ''')


class IGE(commands.Cog):
    """Idea Groups Expanded"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def ige(self, ctx):
        """Returns the IGE steam page"""
        if ctx.invoked_subcommand is None:
            ige_embed = embedMaker.embedMaker('Idea Groups Expanded',
                                             'https://steamcommunity.com/sharedfiles/filedetails/?id=1870443785',
                                             'The future is now, IV', 0x531b93, 'Made by Boss',
                                             'https://steamuserimages-a.akamaihd.net/ugc/785239613537944566/3F30827F8EA8C40AE769B96B4470EDCAD5DEBBFF/')
            await ctx.send(embed=ige_embed.t)

    @ige.command()
    async def find(self, ctx, idea: str):
        """Returns an idea group"""
        desc = ""
        for x, y in data2.items():
            x = x.replace("_idea_groups_expanded", "").replace("_", " ").title()
            if x.startswith(idea.title()):
                desc += x + '\n'
                for a, b in y.items():
                    b = str(b).replace("{", "").replace("}", "").replace("'", "")
                    a = a.replace("_", " ").title()
                    if a == 'Category':
                        temp = f'     {a}: {b}\n'
                        desc += temp
                    else:
                        desc += a + '\n'
                        b = "     " + b + '\n'
                        desc += b
        await ctx.send(desc)


class ExpandedMods(commands.Cog):
    """All expanded mods"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def expanded_mods(self, ctx):
        """Returns the expanded collection page"""
        if ctx.invoked_subcommand is None:
            ige_embed = embedMaker.embedMaker('Made by the Expanded, for the Expanded', 'https://steamcommunity.com'
                                                                                        '/workshop/filedetails/?id'
                                                                                        '=1626860092', 'Hopefully '
                                                                                                       'Europa '
                                                                                                       'Expanded',
                                              0x531b93, 'Europa Expanded?',
                                              'https://steamuserimages-a.akamaihd.net/ugc/791991207699354490'
                                              '/DEEAF52208A77B4B42ABFF5CF68AF88F883A9BBB/')
            await ctx.send(embed=ige_embed.t)


def setup(bot):
    # bot.add_cog(wu(bot))
    bot.add_cog(DVE(bot))
    bot.add_cog(IGE(bot))
    bot.add_cog(ExpandedMods(bot))
