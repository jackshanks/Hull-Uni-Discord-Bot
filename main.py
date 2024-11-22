import nextcord
import os
from Config.ConfigLoader import Config
from nextcord.ext import commands
from Bot.Cogs.Managers.QuoteManager import QuoteManager
from Bot.Cogs.Commands.QuoteCommands import QuoteCommands
from Bot.Cogs.Commands.ColourCommands import ColourCommands
from Bot.Cogs.Commands.BasicCommands import BasicCommands
from Bot.Cogs.Commands.ConfigCommands import ConfigCommands
from Database import DatabaseHandler

Config()
print(Config.guild_ids)

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

db = DatabaseHandler.DatabaseHandler()


@bot.event
async def on_ready():
    bot.add_cog(QuoteCommands(bot, db))
    bot.add_cog(ColourCommands(bot, db))
    bot.add_cog(QuoteManager(bot, db))
    bot.add_cog(BasicCommands(bot, db))
    bot.add_cog(ConfigCommands(bot, db))
    bot.add_all_cog_commands()
    await bot.sync_all_application_commands()
    print("ready")


@bot.event
async def on_shutdown():
    await db.close()


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
