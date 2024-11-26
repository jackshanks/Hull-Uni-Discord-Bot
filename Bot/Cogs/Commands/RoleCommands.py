from nextcord.ext import commands
from nextcord import Interaction
import nextcord

from Bot.Cogs.Managers.DropdownManager import DropdownView
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config


class RoleCommands(BaseCog):
    @nextcord.slash_command(name="assign-colour", description="Assign yourself a colour", guild_ids=Config().guild_ids)
    async def assign_colour(self, interaction: Interaction):
        await interaction.response.send_message("Select a new colour", view=DropdownView(interaction, role_type="colour"),ephemeral=True)

    @nextcord.slash_command(name="remove-colour", description="Go back to your default colour",guild_ids=Config().guild_ids)
    async def remove_all_colour(self, interaction: Interaction):
        for i in interaction.user.roles:
            if i.id in Config().colour:
                await interaction.user.remove_roles(i)
        await interaction.send(":+1: Your colour has been reset", ephemeral=True)

    @nextcord.slash_command(name="assign-game", description="Give yourself game roles!", guild_ids=Config().guild_ids)
    async def assign_game(self, interaction: Interaction):
        await interaction.response.send_message("Select new game(s)", view=DropdownView(interaction, role_type="game"), ephemeral=True)

    @nextcord.slash_command(name="remove-games", description="Remove all your game roles!", guild_ids=Config().guild_ids)
    async def remove_games(self, interaction: Interaction):
        for i in interaction.user.roles:
            if i.id in Config().game:
                await interaction.user.remove_roles(i)
        await interaction.send(":+1: Your games have been reset", ephemeral=True)
