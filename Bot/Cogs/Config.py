from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from nextcord.ext import application_checks
from Config import ConfigLoader

class ConfigCommands(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    @nextcord.slash_command(name="reloadconfig",description="")
    @application_checks.has_permissions(administrator=True)
    async def reloadconfig(self,ctx):
        ConfigLoader.Config.LoadConfig()
        ctx.send("Done")