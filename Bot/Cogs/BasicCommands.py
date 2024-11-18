from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Config import ConfigLoader


class BasicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    testserverid = 554737777049206794

    @nextcord.slash_command(name="ping", description="Find out the response time of the bot", guild_ids=[testserverid])
    async def ping(self, ctx):
        return await ctx.response.send_message(f'Pong! {round(ctx.client.latency * 1000)} ms')

    @nextcord.slash_command(name="help", description="Get help with bot commands", guild_ids=[testserverid])
    async def ping(self, ctx):
        return await ctx.response.send_message(
            'https://docs.google.com/document/d/1UtepVatMgyV7riBK9gXyhrvnkCMSEVjm94jsOq3Lzek/edit?usp=sharing')
