from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Config import ConfigLoader
from Database import DatabaseHandler


class QuoteCommands(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    testserverid = 554737777049206794

    @nextcord.slash_command(name="get-random-quote", description="Get a random quote!", guild_ids=[testserverid])
    async def get_random_quote(self, ctx):
        result = await self.db.get_quote()
        return await ctx.response.send_message(result)
