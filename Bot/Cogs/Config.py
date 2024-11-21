from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from nextcord.ext import application_checks
from Config import ConfigLoader
import datetime

testserverid = 554737777049206794

class ConfigCommands(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="reloadconfig",description="reloads the config",guild_ids=[testserverid])
    @application_checks.has_permissions(administrator=True)
    async def reloadconfig(self,ctx:Interaction):
        ConfigLoader.Config.LoadConfig()
        print(f"Config reloaded at {datetime.datetime.now()} by {ctx.user.name}({ctx.user.id})")
        await ctx.response.send_message("done",ephemeral=True)