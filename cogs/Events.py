import discord
from discord.ext import commands
import random




#name mentions
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.index = random.randint(1,8)
    member = discord.Member

    #login
    #random pings
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user: return
        content = message.content
        if content.lower() == 'ping': await message.channel.send('Pong!')
        if content == '/o/': await message.channel.send('\\o\\')
        if content == '\\o\\': await message.channel.send('/o/')
        if content == 'o/': await message.channel.send('o7')
        if content == '\\o': await message.channel.send('o7')



    #member joining:
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcomeMessage = ['Military master? Diplomatic Devil? Administrative assistant? No! He\'s none other than {}',
        '{} has a vision that spans far and wide, but since this is a 2D game, he can only view widely',
        'Legends say that {} has a father that smells of elder berries',
        '{} has joined the coalition!',
        '{} converted to the one and only true faith!',
        '{} has been added to the Expanded Mod Empire. Rumor has it that they seek protection from Waifu Universalis!',
        'You\'re finally awake {}. You were trying to join the Holy Roman Empire, same as us. Walked right into that French ambush',
        'The throne of {} has just married into our dynasty. Take that von Habsburgs!',
        '{} has joined the trade league. Such is life.',
        'Welcome to the rice tields {}',
        'Expanded Team now has a recruitment casus belli on {}',]
        guild = member.guild
        if guild.system_channel is not None:
            await guild.system_channel.send(welcomeMessage[self.bot.index].format(str(member.mention)))
        self.bot.index = (self.bot.index + 1) % 9

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if type(error).__name__ == 'CommandNotFound':
            x = True


def setup(bot):
    bot.add_cog(Events(bot))
