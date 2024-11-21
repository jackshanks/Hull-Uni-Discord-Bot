from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from nextcord.ext import application_checks
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
import datetime


class ConfigCommands(BaseCog):
    @nextcord.slash_command(name="reloadconfig", description="reloads the config", guild_ids=Config().guild_ids)
    @application_checks.has_permissions(administrator=True)
    async def reloadconfig(self, ctx: Interaction):
        Config().config.LoadConfig()
        print(f"Config reloaded at {datetime.datetime.now()} by {ctx.user.name}({ctx.user.id})")
        await ctx.response.send_message("done", ephemeral=True)
