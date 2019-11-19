import discord
from discord.ext import commands


class embedMaker:
    def __init__(self, title, url, description, color, name, picture):
        self.t = discord.Embed(title=title, url=url, description=description, color=color)
        self.t = self.t.set_author(name=name)
        self.t = self.t.set_thumbnail(url=picture)
