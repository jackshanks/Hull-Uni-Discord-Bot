import nextcord
import nextcordwavelink as wavelink

async def create_track_embed(track: wavelink.Playable, original) -> nextcord.Embed:
    """Helper method to create track information embed."""
    embed: nextcord.Embed = nextcord.Embed(title="Now Playing")
    embed.description = f"**{track.title}** by `{track.author}`"

    if track.artwork:
        embed.set_image(url=track.artwork)

    if original and original.recommended:
        embed.description += f"\n\n`This track was recommended via {track.source}`"

    if track.album.name:
        embed.add_field(name="Album", value=track.album.name)

    return embed
