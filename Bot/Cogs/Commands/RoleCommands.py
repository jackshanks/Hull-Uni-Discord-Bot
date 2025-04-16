from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Bot.Cogs.Managers.DropdownManager import PersistentRoleView
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config


class RoleCommands(BaseCog):
    ROLE_CHANNEL_ID = 1359604047803449454

    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.persistent_view_added = False
        self.db = db

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(PersistentRoleView(self.db))

        if not self.persistent_view_added:
            channel = self.bot.get_channel(self.ROLE_CHANNEL_ID)
            if channel:
                await channel.purge(limit=5)

                await channel.send("**Role Selection**\nChoose your colour and game roles below:", view=PersistentRoleView(self.db))
                self.persistent_view_added = True
                print(f"Persistent role view added to channel {self.ROLE_CHANNEL_ID}")
            else:
                print(f"Could not find channel with ID {self.ROLE_CHANNEL_ID}")

    @nextcord.slash_command(name="refresh-role-menu", description="Refresh the role selection menu", guild_ids=Config().guild_ids)
    @commands.has_permissions(administrator=True)
    async def refresh_role_menu(self, interaction: Interaction):
        channel = self.bot.get_channel(self.ROLE_CHANNEL_ID)
        if channel:
            await channel.purge(limit=5)
            await channel.send("**Role Selection**\nChoose your colour and game roles below:", view=PersistentRoleView(self.db))
            await interaction.response.send_message("Role menu refreshed!", ephemeral=True)
        else:
            await interaction.response.send_message(f"Could not find channel with ID {self.ROLE_CHANNEL_ID}", ephemeral=True)