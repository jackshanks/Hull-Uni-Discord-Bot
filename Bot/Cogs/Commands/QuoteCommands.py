from nextcord import Interaction
import nextcord
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
from Bot.Cogs.Managers import QuoteManager


class QuoteCommands(BaseCog):
    @nextcord.slash_command(name="get-random-quote", description="Get a random quote!", guild_ids=Config().guild_ids)
    async def get_random_quote(self, ctx):
        result = await self.db.execute("""SELECT * FROM quotes ORDER BY DBMS_RANDOM.VALUE FETCH FIRST 1 ROW ONLY""")
        return await ctx.response.send_message(result)

    @nextcord.slash_command(name="submit-quote", description="Submit a quote.", guild_ids=Config().guild_ids)
    async def submit_quote(self, ctx: Interaction, quote: str, said_by: nextcord.Member):
        quoted_by = ctx.user
        chan = self.bot.get_channel(Config().quote_channels[1])
        e = await QuoteManager.create_quote_embed(quote, said_by, quoted_by)
        x = await chan.send(embed=e)
        try:
            await self.db.execute("""INSERT INTO quotes (id, quote, said_by, quoted_by, deleted, star)
                    VALUES (:1, :2, :3, :4, 0, 0)""", (x.id, quote, said_by.id, quoted_by.id))
            return await ctx.response.send_message("Quote Submitted", ephemeral=True)
        except Exception as e:
            return await ctx.response.send_message(f"error saving quote: {quote}-{e}", ephemeral=True)
