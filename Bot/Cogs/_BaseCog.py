from nextcord.ext import commands
from Config.ConfigLoader import Config


class BaseCog(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        config = Config()
        self.guild_ids = config.guild_ids
