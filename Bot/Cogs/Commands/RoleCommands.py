from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Bot.Cogs.Managers.DropdownManager import ColourRoleView, GameRoleView
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config


class RoleCommands(BaseCog):
    ROLE_CHANNEL_ID = 1359604047803449454

    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.persistent_view_added = False
        self.db = db

    @nextcord.slash_command(name="refresh-role-menu", description="Refresh the role selection menu", guild_ids=Config().guild_ids)
    @commands.has_permissions(administrator=True)
    async def refresh_role_menu(self, interaction: Interaction):
        colour_view = ColourRoleView(self.db)
        await colour_view.setup_items()
        self.bot.add_view(colour_view)

        game_view = GameRoleView(self.db)
        await game_view.setup_items()
        self.bot.add_view(game_view)

        channel = self.bot.get_channel(self.ROLE_CHANNEL_ID)
        if channel:
            await channel.purge(limit=5)  # Clear previous messages

            colour_message_view = ColourRoleView(self.db)
            await colour_message_view.setup_items()

            colour_embed = nextcord.Embed(
                title="Color Selection",
                description="**Choose your name color**\n\nClick a color button to set your name color. You can have only one color at a time.",
                color=nextcord.Color.blue()
            )

            await channel.send(embed=colour_embed, view=colour_message_view)

            # Create and send game role message
            game_message_view = GameRoleView(self.db)
            await game_message_view.setup_items()

            game_embed = nextcord.Embed(
                title="Game Selection",
                description="**Join game channels**\n\nClick game buttons to join or leave specific game channels. You can join multiple game channels.",
                color=nextcord.Color.green()
            )

            await channel.send(embed=game_embed, view=game_message_view)

            self.persistent_views_added = True
            await interaction.response.send_message("Role menus refreshed successfully!", ephemeral=True)
            print(f"Persistent role views added to channel {self.ROLE_CHANNEL_ID}")
        else:
            await interaction.response.send_message(f"Could not find channel with ID {self.ROLE_CHANNEL_ID}", ephemeral=True)
            print(f"Could not find channel with ID {self.ROLE_CHANNEL_ID}")