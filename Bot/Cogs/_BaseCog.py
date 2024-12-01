from nextcord.ext import commands
from Config.ConfigLoader import Config


class BaseCog(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.config = Config()
        self.guild_ids = self.config.guild_ids
