import discord
from ..Config.ConfigLoader import Config
from discord.ext import commands
from Cogs.QuoteManager import QuoteManager
from Cogs.AssignColour import AssignColour

BOT_TOKEN = ''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    bot.add_cog(QuoteManager(bot))
    bot.add_cog(AssignColour(bot))

Config.LoadConfig()
bot.run(BOT_TOKEN)