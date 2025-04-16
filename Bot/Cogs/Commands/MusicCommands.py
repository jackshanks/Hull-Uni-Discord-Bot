import nextcordwavelink as wavelink
from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from typing import cast
from Bot.Cogs.Managers import MusicManager
from Config.ConfigLoader import Config
from Bot.Cogs._BaseCog import BaseCog


class MusicCommands(BaseCog):
    def __init__(self, bot: commands.Bot, db):
        super().__init__(bot, db)
        self.voice_clients = {}
        self.node = wavelink.Node(uri='http://127.0.0.1:2333', password='password')

    async def cog_load(self) -> None:
        """Set up the Wavelink node when the cog is loaded."""
        try:
            await wavelink.Pool.connect(
                client=self.bot,
                nodes=[self.node],
                cache_capacity=100
            )
            print("Successfully connected to Lavalink node!")
        except Exception as e:
            print(f"Failed to connect to Lavalink node: {e}")

    @nextcord.slash_command(name="play", description="Play a song", guild_ids=Config().guild_ids)
    async def play(self, ctx: Interaction, query: str):
        """Play a song with the given query."""
        if not ctx.guild:
            return

        # Get the voice state of the user
        if not ctx.user.voice:
            await ctx.response.send_message("Please join a voice channel first before using this command.")
            return

        player: wavelink.Player
        player = cast(wavelink.Player, ctx.guild.voice_client)

        if not player:
            try:
                wavelink_player = wavelink.Player(self.bot, ctx.user.voice.channel)
                player = await ctx.user.voice.channel.connect(cls=wavelink_player)
                await player.set_volume(100)
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except nextcord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return

        # partial = AutoPlay songs but no recommendations , disabled = No AutoPlay
        if player.autoplay is None or wavelink.AutoPlayMode.enabled:
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
            await ctx.send(f"{ctx.user.mention} - Could not find any tracks with that query. Please try again.")
            return

        if isinstance(tracks, wavelink.Playlist):
            for track in tracks:
                await player.queue.put_wait(track)

            if "spotify" in query:
                await ctx.send(f"{ctx.user.mention} Added the playlist **`Spotify doesn't send playlist names :)`** to the queue.")
            else:
                await ctx.send(f"{ctx.user.mention} Added the playlist **`{tracks.name}`** to the queue.")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await ctx.send(f"{ctx.user.mention} Added **`{track}`** to the queue.")

        if not player.playing:
            await player.play(player.queue.get())

    @nextcord.slash_command(name="skip", description="Skip a song", guild_ids=Config().guild_ids)
    async def skip(self, ctx: Interaction):
        """Skip the current song."""
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        await ctx.send(f"{player.current.title} skipped by {ctx.user.mention}!")
        await player.skip(force=True)

    @nextcord.slash_command(name="suggested", description="Toggles playing suggested songs", guild_ids=Config().guild_ids)
    async def suggested(self, ctx: Interaction):
        """Skip the current song."""
        player = cast(wavelink.Player, ctx.guild.voice_client)

        if not player:
            try:
                wavelink_player = wavelink.Player(self.bot, ctx.user.voice.channel)
                player = await ctx.user.voice.channel.connect(cls=wavelink_player)
                await player.set_volume(100)
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except nextcord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return

        if player.autoplay == wavelink.AutoPlayMode.partial:
            player.autoplay = wavelink.AutoPlayMode.enabled
        else:
            player.autoplay = wavelink.AutoPlayMode.partial

        await ctx.send(str(player.autoplay))

    @nextcord.slash_command(name="pause_resume", description="Pause/Resume a song", guild_ids=Config().guild_ids)
    async def pause_resume(self, ctx: Interaction):
        """Pause or Resume the Player depending on its current state."""
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        if player.paused:
            await ctx.send(f"Paused by {ctx.user.mention}!")
        else:
            await ctx.send(f"Resumed by {ctx.user.mention}!")

    @nextcord.slash_command(name="clear", description="Clear the queue", guild_ids=Config().guild_ids)
    async def clear_queue(self, ctx: Interaction):
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        player.queue.clear()
        await ctx.send(f"Queue cleared by {ctx.user.mention}!")

    @nextcord.slash_command(name="view", description="View the queue", guild_ids=Config().guild_ids)
    async def view_queue(self, ctx: Interaction):
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        queue = player.queue[:50]  # Slice first 50 tracks
        if len(queue) < 1:
            await ctx.send("The queue is empty")
            return

        tostring = ""
        a = 0
        for i in queue:
            a+=1
            tostring += f"{a}) {i.title}\n"

        if len(player.queue) > 50:
            tostring += f"\n... and {len(player.queue) - 50} more tracks"

        await ctx.send(tostring)

    @nextcord.slash_command(name="shuffle", description="Shuffle the queue", guild_ids=Config().guild_ids)
    async def shuffle(self, ctx: Interaction):
        """Disconnect the Player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        player.queue.shuffle()
        await ctx.send(f"{ctx.user.mention} shuffled the queue!")

    @nextcord.slash_command(name="disconnect", description="Disconnect the bot", guild_ids=Config().guild_ids)
    async def disconnect(self, ctx: Interaction):
        """Disconnect the Player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.guild.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.send(f"{ctx.user.mention} disconnected the bot!")

    @commands.Cog.listener(name="on_wavelink_track_start")
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        player: wavelink.Player | None = payload.player
        if not player:
            # Handle edge cases...
            return

        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = payload.track

        embed = await MusicManager.create_track_embed(track, original)
        await player.home.send(embed=embed)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload) -> None:
        print(f"Track ended: {payload.track.title}")
        print(f"Reason: {payload.reason}")
