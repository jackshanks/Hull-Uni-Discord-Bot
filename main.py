import nextcord
import os
from Config.ConfigLoader import Config
from nextcord.ext import commands
from Bot.Cogs.QuoteManager import QuoteManager
from Bot.Cogs.QuoteCommands import QuoteCommands
from Bot.Cogs.AssignColour import AssignColour
from Bot.Cogs.BasicCommands import BasicCommands
from Database import DatabaseHandler

Config.LoadConfig()
print(Config.config)

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    bot.add_cog(QuoteCommands(bot))
    bot.add_cog(AssignColour(bot))
    bot.add_cog(QuoteManager(bot))
    bot.add_cog(BasicCommands(bot))
    bot.add_all_cog_commands()
    await bot.sync_all_application_commands()
    print("ready")


# Uses environmental variable to get token then displays errors upon bot run
try:
    print(os.getenv("auth"))
    token = os.getenv("auth")
    bot.run(token)
except nextcord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
