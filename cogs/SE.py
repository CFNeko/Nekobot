import discord
from discord.ext import commands
import embedMaker
from bs4 import BeautifulSoup
import asyncpg
import asyncio
import aiohttp

data = dict()

class se(commands.Cog):
    """Subjects Expanded"""
    def __init__(self, bot):
        self.bot = bot
        self.bot.hasUpdated = False
    @commands.group(case_insensitive=True)
    async def se(self, ctx):
        "Returns the SE steam page"
        if ctx.invoked_subcommand is None:
            seEmbed = embedMaker.embedMaker('Subjects Expanded', 'https://steamcommunity.com/sharedfiles/filedetails/?id=1834079712', 'For all your overlording needs', 0xff2600, 'Made by Lemon', 'https://steamuserimages-a.akamaihd.net/ugc/791991207699275639/21257382F358B5F2A6226827AC891A22BAC2C901/')
            await ctx.send(embed=seEmbed.t)
    @se.command()
    async def update(self, ctx):
        """Updates the database"""
        async with self.bot.db.acquire() as conn:
            conn = await asyncpg.connect('postgresql://postgres@localhost/expanded_data')
            await conn.execute('''DELETE FROM se_subjects;
            ALTER SEQUENCE se_subjects_id_seq RESTART WITH 1;
            ''')
            zipper = dict()
            title = list()
            description = list()
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f'https://steamcommunity.com/workshop/filedetails/discussion/1834079712/3647273545685194210/') as r:
                    tree = await r.read()
                soup = BeautifulSoup(tree, 'html.parser')
                tags = soup('div', {'class' : 'bb_h1'})
                tags2 = soup('i')
                for line in tags:
                    title.append(line.contents[0].title())
                for line in tags2:
                    description.append(line.contents[0])
                for x, y in zip(title, description):
                    await conn.execute('''INSERT INTO  se_subjects (subject, description) VALUES ($1, $2)''', x, y)
                await ctx.send('Database updated!')
                self.bot.hasUpdated = False
                await asyncio.sleep(60)
    @se.command()
    async def find(self, ctx,*, subject: str):
        """Finds info on a specific subject (type +se subjects)"""
        try:
            print(f'SE request found! {subject}')
            async with self.bot.db.acquire() as conn:
                result = await conn.fetchval('SELECT description FROM se_subjects WHERE subject = $1', subject.title())
                await ctx.send(str(result))
        except:
            await ctx.send('Neko can\'t find it')
    @se.command()
    async def subjects(self, ctx):
        """Gives back a list of all subjects"""
        global subjectList
        if self.bot.hasUpdated is False:
            async with self.bot.db.acquire() as conn:
                result = await conn.fetch('SELECT subject FROM se_subjects ORDER BY subject')
                print('Creating new list')
                self.bot.hasUpdated = True
                subjectList = ''
                for subject in result:
                    subjectList = (f'{subjectList} \u203B {subject["subject"]}')
                subjectList = subjectList + ' \u203B'
        else:
            print('Sending used list')
        await ctx.send(subjectList)
    @se.command()
    async def info(self, ctx):
        """Gives a link for even more subject info"""
        seEmbedInfo = embedMaker.embedMaker('Subjects Expanded', 'https://steamcommunity.com/workshop/filedetails/discussion/1834079712/3647273545685194210/', 'See the Details', 0xff2600, 'All Subject Data', 'https://steamuserimages-a.akamaihd.net/ugc/791991207699275639/21257382F358B5F2A6226827AC891A22BAC2C901/')
        await ctx.send(embed=seEmbedInfo.t)


def setup(bot):
    bot.add_cog(se(bot))
