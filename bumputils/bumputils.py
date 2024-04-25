import discord

from redbot.core import commands, app_commands, Config

class BumpUtils(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            command="",
            channel=0,
            user={}
        )


    bumputils = app_commands.Group(name="bumputils", description="Zähle wie oft eine Person einen Command genutzt hat")