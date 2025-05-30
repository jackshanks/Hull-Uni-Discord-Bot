﻿import nextcord
from nextcord import Interaction


class ColourRoleView(nextcord.ui.View):
    def __init__(self, db):
        super().__init__(timeout=None)
        self.db = db

    async def setup_items(self):
        # Add color buttons
        try:
            colour_roles = await self.db.execute("SELECT id, name FROM roles WHERE type = 'colour'")
            for role_id, role_name in colour_roles:
                try:
                    self.add_item(ColourButton(self.db, role_id, role_name))
                except Exception as e:
                    print(f"Error adding button for colour role {role_name}: {e}")
        except Exception as e:
            print(f"Failed to load colour roles from database: {e}")


class GameRoleView(nextcord.ui.View):
    def __init__(self, db):
        super().__init__(timeout=None)
        self.db = db

    async def setup_items(self):
        # Add game buttons
        try:
            game_roles = await self.db.execute("SELECT id, name FROM roles WHERE type = 'game'")
            for role_id, role_name in game_roles:
                try:
                    self.add_item(GameButton(self.db, role_id, role_name))
                except Exception as e:
                    print(f"Error adding button for game role {role_name}: {e}")
        except Exception as e:
            print(f"Failed to load game roles from database: {e}")


class ColourButton(nextcord.ui.Button):
    def __init__(self, db, role_id, role_name):
        self.db = db
        self.role_id = role_id
        super().__init__(
            style=nextcord.ButtonStyle.secondary,
            label=role_name,
            custom_id=f"colour_button_{role_id}"
        )

    async def callback(self, interaction: Interaction):
        result = await self.db.execute("SELECT id FROM roles WHERE type = 'colour'")
        colour_role_ids = [row[0] for row in result]

        for role in interaction.user.roles:
            if role.id in colour_role_ids:
                await interaction.user.remove_roles(role)

        # Add the selected color role
        role = interaction.guild.get_role(self.role_id)
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f"You've been given the {role.name} colour!", ephemeral=True)


class GameButton(nextcord.ui.Button):
    def __init__(self, db, role_id, role_name):
        self.db = db
        self.role_id = role_id
        super().__init__(
            style=nextcord.ButtonStyle.secondary,
            label=role_name,
            custom_id=f"game_button_{role_id}"
        )

    async def callback(self, interaction: Interaction):
        role = interaction.guild.get_role(self.role_id)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Removed the {role.name} role!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"You've been given the {role.name} role!", ephemeral=True)


