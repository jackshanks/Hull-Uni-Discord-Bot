from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Config import ConfigLoader

class QuoteCommands(commands.Cog):
    def __init__(self, client, data):
        self.client = client
        self.data = data

    testserverid = 554737777049206794

    @nextcord.slash_command(name="get-random-quote", description="Get a random quote!", guild_ids=[testserverid])
    async def get_random_quote(self, ctx):
        return await ctx.response.send_message(self.data.get_quote())
