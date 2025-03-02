import nextcord
import os

from Bot.Cogs.Commands.MusicCommands import MusicCommands
from Bot.Cogs.Managers.RulesManager import RuleManager
from Config.ConfigLoader import Config
from nextcord.ext import commands
from Bot.Cogs.Managers.QuoteManager import QuoteManager
from Bot.Cogs.Commands.QuoteCommands import QuoteCommands
from Bot.Cogs.Commands.RoleCommands import RoleCommands
from Bot.Cogs.Commands.BasicCommands import BasicCommands
from Bot.Cogs.Commands.AdminCommands import AdminCommands
from Database import DatabaseHandler

Config()

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)
db = DatabaseHandler.DatabaseHandler()


@bot.event
async def on_ready():
    bot.add_cog(QuoteCommands(bot, db))
    bot.add_cog(RoleCommands(bot, db))
    # bot.add_cog(QuoteManager(bot, db))
    bot.add_cog(BasicCommands(bot, db))
    bot.add_cog(AdminCommands(bot, db))
    rule_cog = RuleManager(bot, db)
    await rule_cog.on_run_rules()
    bot.add_cog(rule_cog)
    music_cog = MusicCommands(bot, db)
    await music_cog.cog_load()
    bot.add_cog(music_cog)
    bot.add_all_cog_commands()
    await bot.sync_all_application_commands()
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="talk tuah"),
                              status=nextcord.Status.do_not_disturb)
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
