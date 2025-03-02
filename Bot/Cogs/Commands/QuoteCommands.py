from nextcord.ext import commands
from nextcord import Interaction
import nextcord

from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
from Database import DatabaseHandler


class QuoteCommands(BaseCog):
    @nextcord.slash_command(name="get-random-quote", description="Get a random quote!", guild_ids=Config().guild_ids)
    async def get_random_quote(self, ctx):
        result = await self.db.get_quote()
        return await ctx.response.send_message(result)
    @nextcord.slash_command(name="submit-quote",description="Get a random quote!", guild_ids=Config().guild_ids)
    async def submit_quote(self,ctx:Interaction, quote:str, saidby:nextcord.Member ):
        chan = self.bot.get_channel(Config().quote_channels[0])
        e = nextcord.Embed(description=quote)
        x = await chan.send(embed=e)
        try:
            await self.db.submit_quote(x.id,quote,saidby.id,saidby.id)
            return await ctx.response.send_message("complete")
        except Exception as e:
            return await ctx.response.send_message(f"error saving quote: {quote }-{ e}")
        