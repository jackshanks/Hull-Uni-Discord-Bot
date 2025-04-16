import nextcord
from nextcord import Interaction
from Config.ConfigLoader import Config


class PersistentRoleView(nextcord.ui.View):
    def __init__(self, db):
        super().__init__(timeout=None)  # Set timeout to None for persistent view
        self.db = db
        self.add_item(ColourDropdown(db))
        self.add_item(GameDropdown(db))


class ColourDropdown(nextcord.ui.Select):
    def __init__(self, db):
        self.db = db
        select_options = []

        colour_roles = self.db.execute("SELECT id, name FROM roles WHERE type = 'colour'")
        for role_id, role_name in colour_roles:
            try:
                select_options.append(nextcord.SelectOption(
                    label=role_name,
                    value=str(role_id)
                ))
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
        colour_role_ids = [row[0] for row in self.db.execute(
            "SELECT id FROM roles WHERE type = 'colour'")]

        for role in interaction.user.roles:
            if role.id in colour_role_ids:
                await interaction.user.remove_roles(role)

        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You've been given the {role.name} colour!", ephemeral=True)

class GameDropdown(nextcord.ui.Select):
    def __init__(self, db):
        self.db = db
        select_options = []

        game_roles = self.db.execute("SELECT id, name FROM roles WHERE type = 'game'")

        for role_id, role_name in game_roles:
            try:
                select_options.append(nextcord.SelectOption(
                    label=role_name,
                    value=str(role_id),
                    description=f"Access to {role_name} channel"
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
