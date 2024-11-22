import wavelink
from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from typing import cast
from nextcord.ext import application_checks
from Bot.Cogs._BaseCog import BaseCog
from Config.ConfigLoader import Config
import datetime

from Bot.Cogs._BaseCog import BaseCog


class MusicCommands(BaseCog):
    def __init__(self, bot: commands.Bot, db):
        super().__init__(bot, db)
        self.voice_clients = {}
        self.node = [wavelink.Node(uri="http:// localhost:8081", password="password")]

    async def connect(self):
        await wavelink.Pool.connect(nodes=self.node, client=self.bot, cache_capacity=100)

    @nextcord.slash_command(name="play", description="Play a song", guild_ids=Config().guild_ids)
    async def play(self, ctx: Interaction, query: str):
        """Play a song with the given query."""
        if not ctx.guild:
            return

        await self.connect()

        # Get the voice state of the user
        if not ctx.user.voice:
            await ctx.response.send_message("Please join a voice channel first before using this command.")
            return

        player: wavelink.Player
        player = cast(wavelink.Player, ctx.guild.voice_client)

        if not player:
            try:
                player = await ctx.user.voice.channel.connect()
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except nextcord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return

        # partial = AutoPlay songs but no recommendations , disabled = No AutoPlay
        player.autoplay = wavelink.AutoPlayMode.partial

        # Lock the player to this channel...
        if not hasattr(player, "home"):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            await ctx.send(
                f"You can only play songs in {player.home.mention}, as the player has already started there.")
            return

        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if not tracks:
            await ctx.send(f"{ctx.message.author.mention} - Could not find any tracks with that query. Please try again.")
            return

        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await ctx.send(f"Added **`{track}`** to the queue.")

        if not player.playing:
            await player.play(player.queue.get(), volume=30)

    @nextcord.slash_command(name="skip", description="Skip a song", guild_ids=Config().guild_ids)
    async def skip(self, ctx: Interaction):
        """Skip the current song."""
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")

    @nextcord.slash_command(name="pause_resume", description="Pause/Resume a song", guild_ids=Config().guild_ids)
    async def pause_resume(self, ctx: Interaction):
        """Pause or Resume the Player depending on its current state."""
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        await ctx.message.add_reaction("\u2705")

    @nextcord.slash_command(name="disconnect", description="Disconnect the bot", guild_ids=Config().guild_ids)
    async def disconnect(self, ctx: Interaction):
        """Disconnect the Player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.message.add_reaction("\u2705")

    @commands.Cog.listener(name="on_wavelink_track_start")
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed: nextcord.Embed = nextcord.Embed(title="Now Playing")
        embed.description = f"**{track.title}** by `{track.author}`"

        if track.artwork:
            embed.set_image(url=track.artwork)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        if track.album.name:
            embed.add_field(name="Album", value=track.album.name)

        await player.home.send(embed=embed)
