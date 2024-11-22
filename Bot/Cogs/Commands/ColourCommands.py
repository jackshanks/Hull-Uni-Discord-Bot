from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config


class ColourCommands(BaseCog):
    @nextcord.slash_command(name="assign-colour", description="Assign yourself a colour", guild_ids=Config().guild_ids)
    async def assign_colour(self, interaction: Interaction):
        for i in interaction.user.roles:
            if i.id in Config().colour:
                await interaction.user.remove_roles(i)
        await interaction.response.send_message("Select new colour", view=DropdownView(interaction), ephemeral=True)

    @nextcord.slash_command(name="remove-colour", description="Go back to your default colour", guild_ids=Config().guild_ids)
    async def remove_all_colour(self, interaction: Interaction):
        for i in interaction.user.roles:
            if i.id in Config().colour:
                await interaction.user.remove_roles(i)
        await interaction.send(":+1: Your colour has been reset", ephemeral=True)


class DropdownView(nextcord.ui.View):
    def __init__(self, interaction):
        super().__init__()
        self.timeout = 30.0
        self.add_item(ColourDropdown(interaction))


class ColourDropdown(nextcord.ui.Select):
    def __init__(self, interaction: Interaction = None):
        select_options = []
        for i in Config().colour:
            try:
                role = interaction.guild.get_role(i)
                select_options.append(nextcord.SelectOption(label=role.name, description=str(role.colour)))
            except:
                continue
        super().__init__(placeholder="none", min_values=1, max_values=1, options=select_options)

    async def callback(self, interaction: Interaction) -> None:
        role = nextcord.utils.get(interaction.guild.roles, name=self.values[0])
        await interaction.user.add_roles(role)
