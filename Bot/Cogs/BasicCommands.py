from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config


class BasicCommands(BaseCog):
    @nextcord.slash_command(name="ping", description="Find out the response time of the bot", guild_ids=Config().guild_ids)
    async def ping(self, ctx):
        return await ctx.response.send_message(f'Pong! {round(ctx.bot.latency * 1000)} ms')

    @nextcord.slash_command(name="help", description="Get help with bot commands", guild_ids=Config().guild_ids)
    async def help(self, ctx):
        return await ctx.response.send_message(
            'https://docs.google.com/document/d/1UtepVatMgyV7riBK9gXyhrvnkCMSEVjm94jsOq3Lzek/edit?usp=sharing')
