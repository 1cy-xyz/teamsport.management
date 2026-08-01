import discord
from datetime import datetime

from config import EMBED_COLOR


def success(
    title: str,
    description: str = "",
    *,
    footer: str = "Staff Management Bot"
) -> discord.Embed:
    """Green success embed."""

    embed = discord.Embed(
        title=f"✅ {title}",
        description=description,
        colour=discord.Colour.green(),
        timestamp=datetime.utcnow()
    )

    embed.set_footer(text=footer)

    return embed


def error(
    title: str,
    description: str = "",
    *,
    footer: str = "Staff Management Bot"
) -> discord.Embed:
    """Red error embed."""

    embed = discord.Embed(
        title=f"❌ {title}",
        description=description,
        colour=discord.Colour.red(),
        timestamp=datetime.utcnow()
    )

    embed.set_footer(text=footer)

    return embed


def warning(
    title: str,
    description: str = "",
    *,
    footer: str = "Staff Management Bot"
) -> discord.Embed:
    """Orange warning embed."""

    embed = discord.Embed(
        title=f"⚠️ {title}",
        description=description,
        colour=discord.Colour.orange(),
        timestamp=datetime.utcnow()
    )

    embed.set_footer(text=footer)

    return embed


def info(
    title: str,
    description: str = "",
    *,
    footer: str = "Staff Management Bot"
) -> discord.Embed:
    """Blue information embed."""

    embed = discord.Embed(
        title=f"ℹ️ {title}",
        description=description,
        colour=EMBED_COLOR,
        timestamp=datetime.utcnow()
    )

    embed.set_footer(text=footer)

    return embed


def leaderboard(title: str) -> discord.Embed:
    """Leaderboard embed."""

    embed = discord.Embed(
        title=f"🏆 {title}",
        colour=discord.Colour.gold(),
        timestamp=datetime.utcnow()
    )

    embed.set_footer(text="Updates live")

    return embed


def session(
    title: str,
    *,
    host: str,
    track: str,
    time: str
) -> discord.Embed:
    """Session panel embed."""

    embed = discord.Embed(
        title=f"🏁 {title}",
        colour=discord.Colour.blurple(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="Host",
        value=host,
        inline=True
    )

    embed.add_field(
        name="Track",
        value=track,
        inline=True
    )

    embed.add_field(
        name="Session Time",
        value=time,
        inline=False
    )

    embed.add_field(
        name="Attending",
        value="0",
        inline=True
    )

    embed.add_field(
        name="Unavailable",
        value="0",
        inline=True
    )

    embed.set_footer(
        text="Use the buttons below to respond."
    )

    return embed
