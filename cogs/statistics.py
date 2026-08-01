import discord
from discord import app_commands
from discord.ext import commands

from database.statistics import get_statistics
from utils.embeds import info
from config import STAFF_ROLE_ID


def format_time(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    return f"{hours}h {minutes}m"


class Statistics(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="statistics",
        description="View staff statistics."
    )
    async def statistics(
        self,
        interaction: discord.Interaction
    ):

        if not self.is_staff(interaction.user):

            await interaction.response.send_message(
                "❌ You must have the Staff role to use this command.",
                ephemeral=True
            )
        
            return

        stats = await get_statistics()

        average = "0h"

        if stats["staff"] > 0:

            average = format_time(
                stats["lifetime"] // stats["staff"]
            )

        embed = info(
            "Staff Statistics"
        )

        embed.add_field(
            name="👥 Registered Staff",
            value=str(stats["staff"]),
            inline=True
        )

        embed.add_field(
            name="🟢 Currently On Duty",
            value=str(stats["active"]),
            inline=True
        )

        embed.add_field(
            name="🏁 Sessions Hosted",
            value=str(stats["sessions"]),
            inline=True
        )

        embed.add_field(
            name="🕒 Weekly Hours",
            value=format_time(stats["weekly"]),
            inline=True
        )

        embed.add_field(
            name="📈 Lifetime Hours",
            value=format_time(stats["lifetime"]),
            inline=True
        )

        embed.add_field(
            name="📊 Average Staff Hours",
            value=average,
            inline=True
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Statistics(bot)
    )
