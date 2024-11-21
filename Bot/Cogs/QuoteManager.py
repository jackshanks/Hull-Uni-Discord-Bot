from nextcord.ext import commands
import nextcord
from Config import ConfigLoader
import json
import emoji
import Database
import Database.DatabaseHandler


class QuoteManager(commands.Cog):
    def __init__(self, client: commands.Bot, db):
        self.client = client
        self.db = db

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_reaction(self, payload: nextcord.RawReactionActionEvent):
        if not payload.channel_id in ConfigLoader.Config.config.get("quotechannels"):
            return
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message == None:
            return
        up = 0
        for x in message.reactions:
            if emoji.emojize(':thumbsup:', language='alias') == x.emoji:
                up += 1
        down = 0
        for x in message.reactions:
            if emoji.emojize(':thumbsdown:', language='alias') == x.emoji:
                down += 1
        if down < 1:
            down = 1

        if up >= down * ConfigLoader.Config.config["starratio"]:
            x = Database.DatabaseHandler.DatabaseHandler()
            y = await x.get_quote_starred(payload.message_id)
            if y:
                await x.mark_quote_as_star(payload.message_id)
            starchan = self.client.get_channel(ConfigLoader.Config.config["starquotechannel"])
            e = nextcord.Embed(description=message.content)
            if len(message.mentions) > 0:
                e.set_author(name=message.mentions[0].name)
            await starchan.send("", embed=e)

        if down >= up * ConfigLoader.Config.config["deleteratio"]:
            e = nextcord.Embed(description=message.content)
            e.set_author(name=f"{message.author.name}({message.author.id})")
            delchan = self.client.get_channel(ConfigLoader.Config.config["deletechannel"])
            await delchan.send("", embed=e)
            x = Database.DatabaseHandler.DatabaseHandler()
            await x.mark_quote_as_deleted(payload.message_id)
            await message.delete()
