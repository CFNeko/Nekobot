from discord.ext import commands
import embedMaker
import asyncpg

class MCE(commands.Cog):
	"""Mercenary Commands Expanded"""
	def __init__(self, bot):
		self.bot = bot

		@commands.group(case_insenstive=True)
		async def mce(self, ctx):
			"""Returns MCE steam page"""
			if ctx.invoked_subcommand is None:
				mce_embed = embedMaker.embedMaker('Mercenary Companies Expanded', 'https://steamcommunity.com/workshop/filedetails'
                                                                  '/?id=2125424517', 'Mercenaries at your behest',
                                                                   0x00fdff,
                                             					  'Made by Vara & Uber',
                                             'https://steamuserimages-a.akamaihd.net/ugc/1049849534508701381/B159CC0E84068298D3A785E280AB2DC4EEAACF8F/?imw=268&imh=268&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true' )
				await ctx.send(embed=me_embed.t)
                                             