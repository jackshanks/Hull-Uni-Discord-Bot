from nextcord.ext import commands
from nextcord import Interaction
import nextcord

from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
from Database import DatabaseHandler


class QuoteCommands(BaseCog):
    @nextcord.slash_command(name="get-random-quote", description="Get a random quote!", guild_ids=Config().guild_ids)
    async def get_random_quote(self, ctx):
        result = await self.db.get_quote()
        return await ctx.response.send_message(result)
