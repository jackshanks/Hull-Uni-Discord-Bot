import discord
import os
from ..Config.ConfigLoader import Config
from discord.ext import commands
from Cogs.QuoteManager import QuoteManager
from Cogs.AssignColour import AssignColour

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    bot.add_cog(QuoteManager(bot))
    bot.add_cog(AssignColour(bot))


Config.LoadConfig()

# Uses environmental variable to get token then displays errors upon bot run
try:
    token = os.getenv("auth")
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
