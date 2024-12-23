﻿import nextcord
from nextcord import Interaction
from Config.ConfigLoader import Config


class DropdownView(nextcord.ui.View):
    def __init__(self, interaction, role_type):
        super().__init__()
        self.timeout = 30.0
        if role_type == "colour":
            self.add_item(ColourDropdown(interaction))
        elif role_type == "game":
            self.add_item(GameDropdown(interaction))


class ColourDropdown(nextcord.ui.Select):
    def __init__(self, interaction: Interaction = None):
        select_options = []
        for i in Config().colour:
            try:
                role = interaction.guild.get_role(i)
                select_options.append(nextcord.SelectOption(label=role.name, description=str(role.colour)))
            except Exception as e:
                print(f"Error occurred while using game dropdown menu! {e}")
        super().__init__(placeholder="none", min_values=1, max_values=1, options=select_options)

    async def callback(self, interaction: Interaction) -> None:
        for i in interaction.user.roles:
            if i.id in Config().colour:
                await interaction.user.remove_roles(i)
        role = nextcord.utils.get(interaction.guild.roles, name=self.values[0])
        await interaction.user.add_roles(role)


class GameDropdown(nextcord.ui.Select):
    def __init__(self, interaction: Interaction = None):
        select_options = []
        for i in Config().game:
            try:
                role = interaction.guild.get_role(i)
                select_options.append(nextcord.SelectOption(label=role.name, description=f"Ability to see the {role.name} channel!"))
            except Exception as e:
                print(f"Error occurred while using game dropdown menu! {e}")
                continue
        super().__init__(placeholder="none", min_values=1, max_values=1, options=select_options)

    async def callback(self, interaction: Interaction) -> None:
        role = nextcord.utils.get(interaction.guild.roles, name=self.values[0])
        await interaction.user.add_roles(role)
