from nextcord.ext import commands
import nextcord
from Config import ConfigLoader
import json
import emoji

class QuoteManager(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_reaction(self,payload : nextcord.RawReactionActionEvent):
        if not payload.channel_id in ConfigLoader.Config.config.get("quotechannels"):
            return
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message == None:
            return
        up = 0
        for x in message.reactions:
            if  emoji.emojize(':thumbsup:', language='alias') == x.emoji:
                up+=1
        down = 0
        for x in message.reactions:
            if  emoji.emojize(':thumbsdown:', language='alias') == x.emoji:
                down+=1
        if down <1:
            down = 1
        if up > down * ConfigLoader.Config.config["starratio"]:
            print("star")
        if down > up *ConfigLoader.Config.config["deleteratio"]:
            print("delete")