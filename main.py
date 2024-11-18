import nextcord
import os
from Config.ConfigLoader import Config
from nextcord.ext import commands
from Bot.Cogs.QuoteManager import QuoteManager
from Bot.Cogs.AssignColour import AssignColour

intents = nextcord.Intents.all()
intents.members = True
bot = commands.Bot(intents=intents)

testserverid = 554737777049206794

@bot.event
async def on_ready():
    print("ready")
    bot.add_cog(QuoteManager(bot))
    bot.add_cog(AssignColour(bot))


Config.LoadConfig()

# Uses environmental variable to get token then displays errors upon bot run
try:
    token = os.getenv("auth")
    bot.run(token)
except nextcord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
