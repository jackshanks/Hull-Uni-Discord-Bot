from nextcord import Interaction
import nextcord
from nextcord.ext import application_checks
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
import datetime


class AdminCommands(BaseCog):
    @nextcord.slash_command(name="ban", description="bans", guild_ids=Config().guild_ids)
    @application_checks.has_permissions(administrator=True)
    async def ban(self, ctx: Interaction, query: str):
        try:
            user = await self.bot.fetch_user(int(query))
            await ctx.guild.ban(user)
        except Exception as e:
            print("Error processing command: " + str(e))
            await ctx.response.send_message("Error processing command: " + str(e), ephemeral=True)

    @nextcord.slash_command(name="reload-config", description="reloads the config", guild_ids=Config().guild_ids)
    @application_checks.has_permissions(administrator=True)
    async def reload_config(self, ctx: Interaction):
        try:
            Config().load_config()
            print(f"Config reloaded at {datetime.datetime.now()} by {ctx.user.name}({ctx.user.id})")
            await ctx.response.send_message("200 OK", ephemeral=True)
        except Exception as e:
            print("Error processing command: " + str(e))
            await ctx.response.send_message("Error processing command: " + str(e), ephemeral=True)

    @nextcord.slash_command(name="add-colour", description="Adds a colour role", guild_ids=Config().guild_ids)
    @application_checks.has_permissions(administrator=True)
    async def add_colour(self, ctx: Interaction, query: int):
        try:
            Config().add(query, "colour")
            await ctx.response.send_message("201 Added", ephemeral=True)
        except Exception as e:
            print("Error processing command: " + str(e))
            await ctx.response.send_message("Error processing command: " + str(e), ephemeral=True)

    @nextcord.slash_command(name="add-game", description="Adds a game role", guild_ids=Config().guild_ids)
    @application_checks.has_permissions(administrator=True)
    async def add_game(self, ctx: Interaction, query: int):
        try:
            Config().add(query, "game")
            await ctx.response.send_message("201 Added", ephemeral=True)
        except Exception as e:
            print("Error processing command: " + str(e))
            await ctx.response.send_message("Error processing command: " + str(e), ephemeral=True)

    @nextcord.slash_command(name="remove-colour", description="Removes a colour role", guild_ids=Config().guild_ids)
    @application_checks.has_permissions(administrator=True)
    async def remove_colour(self, ctx: Interaction, query: int):
        try:
            Config().remove(query, "colour")
            await ctx.response.send_message("201 Removed", ephemeral=True)
        except Exception as e:
            print("Error processing command: " + str(e))
            await ctx.response.send_message("Error processing command: " + str(e), ephemeral=True)

    @nextcord.slash_command(name="remove-game", description="Removes a game role", guild_ids=Config().guild_ids)
    @application_checks.has_permissions(administrator=True)
    async def remove_game(self, ctx: Interaction, query: int):
        try:
            Config().add(query, "game")
            await ctx.response.send_message("201 Removed", ephemeral=True)
        except Exception as e:
            print("Error processing command: " + str(e))
            await ctx.response.send_message("Error processing command: " + str(e), ephemeral=True)