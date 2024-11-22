from nextcord.ext import commands
import nextcord

from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
import json
import emoji
import Database.DatabaseHandler
import re


class QuoteManager(BaseCog):
    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_reaction(self, payload: nextcord.RawReactionActionEvent):
        if not payload.channel_id in Config().quote_channels:
            return
        channel = self.bot.get_channel(payload.channel_id)
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

        if up >= down * Config().star_ratio:
            y = await self.db.get_quote_starred(payload.message_id)
            if y:
                await self.db.mark_quote_as_star(payload.message_id)
            star_chan = self.bot.get_channel(Config().star_quote_channel)
            e = nextcord.Embed(description=message.content)
            if len(message.mentions) > 0:
                e.set_author(name=message.mentions[0].name)
            await star_chan.send("", embed=e)

        if down > up * Config().delete_ratio:
            e = nextcord.Embed(description=message.content)
            e.set_author(name=f"{message.author.name}({message.author.id})")
            del_chan = self.bot.get_channel(Config().delete_channel)
            await del_chan.send("", embed=e)
            await self.db.mark_quote_as_deleted(payload.message_id)
            await message.delete()

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: nextcord.Message):
        if message.author == self.bot.user:
            return
        if len(message.mentions) == 0:
            return
        content = message.content
        if content.count("\"") == 0:
            return
        splits = content.split("\"")
        splits = splits[1:]
        for i in range(0, len(splits) // 2):
            i = i * 2
            try:
                await self.db.submit_quote(message.id, splits[i], re.findall("<@[0-9]+>", splits[i + 1])[0],
                                           message.author.id)
            except:
                message.reply(f"error saving quote: {splits[i]}")
