import discord
from discord import app_commands
from discord.ext import commands

from database import duty
from utils.embeds import info
from config import STAFF_ROLE_ID


def format_time(seconds: int):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    return f"{hours}h {minutes}m"


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(
        name="profile",
        description="View your staff profile."
    )
    @app_commands.checks.has_role(STAFF_ROLE_ID)
    async def profile(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        member = member or interaction.user

        profile = await duty.get_profile(member.id)

        if profile is None:

            await interaction.response.send_message(

                embed=info(
                    "Profile",
                    "This staff member has no recorded duty time."
                ),

                ephemeral=True

            )

            return

        username = profile[0]
        total = profile[1]
        weekly = profile[2]
        sessions = profile[3]

        embed = info(
            f"{username}'s Staff Profile"
        )

        embed.set_thumbnail(url=member.display_avatar.url)

        embed.add_field(
            name="🕒 Weekly Hours",
            value=format_time(weekly),
            inline=True
        )

        embed.add_field(
            name="📈 Lifetime Hours",
            value=format_time(total),
            inline=True
        )

        embed.add_field(
            name="🏁 Sessions Attended",
            value=str(sessions),
            inline=True
        )

        active = await duty.get_active_shift(member.id)

        if active:

            status = "🟢 On Duty"

        else:

            status = "🔴 Off Duty"

        embed.add_field(
            name="Current Status",
            value=status,
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Profile(bot)
    )
