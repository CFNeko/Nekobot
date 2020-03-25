from discord.ext import commands
import embedMaker
import json
import asyncpg
import aiohttp
import os

BOT_ADMIN_SERVER = os.getenv('BOT_ADMIN_SERVER')
BOT_ADMIN_CHAN = os.getenv('BOT_ADMIN_CHAN')


def _is_admin(ctx):
    return ctx.author.guild.name == BOT_ADMIN_SERVER and ctx.channel.name == BOT_ADMIN_CHAN


class ADM(commands.Cog):
    """Missions Expanded"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)
    async def adm(self, ctx):
        """Returns the ME steam page"""
        if ctx.invoked_subcommand is None:
            me_embed = embedMaker.embedMaker('admin the bot', 'https://steamcommunity.com/sharedfiles/filedetails'
                                                                  '/?id=1349005102', 'Missions to feed your '
                                                                                     'families', 0x00fdff,
                                             'VERY restricted',
                                             'https://steamuserimages-a.akamaihd.net/ugc/785237978963961829'
                                             '/6FA7A17EA9C6211FC4DCC04D49EBDB908FFDA727/?imw=268&imh=268&ima=fit'
                                             '&impolicy=Letterbox&imcolor=%23000000&letterbox=true')
            await ctx.send(embed=me_embed.t)

    @adm.command()
    async def me_add(self, ctx, *, args: str):
        """add a mission entry, but ONLY if you're admin"""
        async with self.bot.db.acquire() as conn:
            if _is_admin(ctx):
                params_array = args.split(" ")
                tag = params_array[0]
                is_me = params_array[-1].lower() == "true"
                name = " ".join(params_array[1:-1])
                result = await conn.fetch('SELECT * FROM tags WHERE tag=$1', tag)
                try:
                    # TODO find out WHY search by tag is all right, but not search by name. (potentially linked, the id isn't the right one)
                    if len(result) == 0:
                        #it is not edit
                        result = await conn.fetch('INSERT INTO  tags (tag, country, me_tag) VALUES ($1, $2, $3)', tag, name, is_me)
                        print(result)
                    else:
                        await conn.fetch('UPDATE tags SET country=$1, me_tag=$2 WHERE tag=$3', name, is_me, tag)
                except Exception as err:
                    print(err)
                await ctx.send(f"Database updated with the tag : {tag}, the name : {name} and is_me set to {is_me}")
            else:
                await ctx.send("GET OUT, peasant! (but nice try)")

    @adm.command()
    async def me_suppress(self, ctx, tag_to_delete: str):
        """suppress a mission entry, but ONLY if you're admin"""
        async with self.bot.db.acquire() as conn:
            if _is_admin(ctx):
                await conn.fetch('DELETE FROM tags WHERE tag = $1', tag_to_delete)
                await ctx.send(f"Database updated by suppressing the tag : {tag_to_delete}")
            else:
                await ctx.send("GET OUT, peasant! (but nice try)")


def setup(bot):
    bot.add_cog(ADM(bot))
