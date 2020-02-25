from discord.ext import commands
import embedMaker
from bs4 import BeautifulSoup
import asyncio
import aiohttp


class TGE(commands.Cog):
    """Trade Goods Expanded"""
    def __init__(self, bot):
        self.bot = bot
    @commands.group(case_insensitive=True)
    async def tge(self, ctx):
        """Returns the TGE steam page"""
        if ctx.invoked_subcommand is None:
            tgeEmbed = embedMaker.embedMaker('Trade Goods Expanded', 'https://steamcommunity.com/sharedfiles/filedetails/?id=1770950522', 'Actual trade', 0x00fdff, 'Made by MrMarcinQ', 'https://i.imgur.com/zbIgVWt.jpg')
            await ctx.send(embed=tgeEmbed.t)
    @tge.command()
    async def find(self, ctx, *, good: str):
        """Finds a specific TGE good (+tge find [good])"""
        async with self.bot.db.acquire() as conn:
            print(f'TGE request found! {good}')
            try:
                result = await conn.fetchrow('SELECT good, price, province_bonus, leader_bonus FROM tge_goods WHERE good = $1', good.title())
                message = '```'
                for tag in result:
                    message = f'{message} {tag} \n'
                message = f'{message}```'
                await ctx.send(message)
            except:
                await ctx.send('Are you sure it exists? Check !tge goods to check it out first')
    @tge.command()
    async def goods(self, ctx):
        """Gives back a list of all TGE trade goods"""
        async with self.bot.db.acquire() as conn:
            goodList = ''
            tgeData = await conn.fetch('SELECT good FROM tge_goods ORDER by good')
            for good in tgeData:
                goodList = f'{goodList} \u203B {good["good"]}'
            goodList = goodList + ' \u203B'
            await ctx.send(goodList)
    @tge.command()
    async def navarra(self, ctx):
        """Concerning why Navarra has whaling as a trade good"""
        await ctx.send('1. The Basque region was known for whaling.\n2. This is PDX\'s fault since they redrew their map borders.\n3. Navarra was not landlocked historically.')
    @tge.command()
    async def update(self, ctx):
        """Updates the TGE database"""
        async with self.bot.db.acquire() as conn:
            await conn.execute('''DELETE FROM tge_goods;
            ALTER SEQUENCE tge_goods_id_seq RESTART WITH 1;''')
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://steamcommunity.com/workshop/filedetails/discussion/1770950522/1636417554415571648/') as r:
                    tree = await r.read()
            soup = BeautifulSoup(tree,'html.parser')
            tag = soup('div', {'class':'bb_h1'})
            for line in tag:
                price = line.next_sibling
                pBonus = price.next_sibling
                await conn.execute('''INSERT INTO  tge_goods (good, price, province_bonus, leader_bonus)
                VALUES ($1, $2, $3, $4)''', line.contents[0], price, pBonus.contents[0], pBonus.contents[1].contents[0])
            await asyncio.sleep(60)


def setup(bot):
    bot.add_cog(TGE(bot))
