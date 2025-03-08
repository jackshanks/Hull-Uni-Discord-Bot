from aiohttp.hdrs import AUTHORIZATION
from nextcord.ext import commands
import nextcord
from oracledb.base_impl import Description

from Bot.Cogs.Managers.DropdownManager import ColourDropdown
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
import json
import emoji
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

        if up > down * Config().star_ratio:
            y = await self.db.get_quote_starred(payload.message_id)
            if y:
                await self.db.mark_quote_as_star(payload.message_id)
            star_chan = self.bot.get_channel(Config().star_quote_channel)
            e = nextcord.Embed(description=message.content)
            if len(message.mentions) > 0:
                e.set_author(name=message.mentions[0].name)
            await star_chan.send("", embed=e)

        if down > up * Config().delete_ratio:
            e = message.embeds[0]
            e.set_author(name=f"{message.author.name}({message.author.id})")
            del_chan = self.bot.get_channel(Config().delete_channel)
            await del_chan.send("", embed=e)
            await self.db.execute("""DELETE FROM quotes WHERE id=:1""", payload.message_id)
            await message.delete()


async def create_quote_embed(quote, said_by, quoted_by) -> nextcord.Embed:
    """Helper method to create track information embed."""
    colour = 0x3498db
    embed: nextcord.Embed = nextcord.Embed(title=f"**'{quote}'**", colour=colour)
    embed.set_footer(text=f"Quoted by {quoted_by.display_name}")
    embed.set_author(name=f"{said_by.display_name}", icon_url=said_by.display_avatar.url)
    return embed
