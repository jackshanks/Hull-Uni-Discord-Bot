import nextcord
from nextcord import Interaction
from Config.ConfigLoader import Config


class PersistentRoleView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Set timeout to None for persistent view
        self.add_item(ColourDropdown())
        self.add_item(GameDropdown())


class ColourDropdown(nextcord.ui.Select):
    def __init__(self):
        select_options = []
        for i in Config().colour:
            try:
                select_options.append(nextcord.SelectOption(label=f"Colour {i}", value=str(i)))
            except Exception as e:
                print(f"Error occurred while setting up colour dropdown menu! {e}")

        super().__init__(
            placeholder="Select a colour",
            min_values=1,
            max_values=1,
            options=select_options,
            custom_id="colour_dropdown"
        )

    async def callback(self, interaction: Interaction) -> None:
        for i in interaction.user.roles:
            if i.id in Config().colour:
                await interaction.user.remove_roles(i)

        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You've been given the {role.name} colour!", ephemeral=True)


class GameDropdown(nextcord.ui.Select):
    def __init__(self):
        select_options = []
        for i in Config().game:
            try:
                # We can't access the guild here, so we'll get the role in the callback
                select_options.append(nextcord.SelectOption(
                    label=f"Game {i}",
                    value=str(i),
                    description=f"Access to game channel"
                ))
            except Exception as e:
                print(f"Error occurred while setting up game dropdown menu! {e}")
                continue

        super().__init__(
            placeholder="Select a game",
            min_values=1,
            max_values=1,
            options=select_options,
            custom_id="game_dropdown"
        )

    async def callback(self, interaction: Interaction) -> None:
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Removed the {role.name} role!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You've been given the {role.name} role!", ephemeral=True)