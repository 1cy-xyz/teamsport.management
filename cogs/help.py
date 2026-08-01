import discord
from discord import app_commands
from discord.ext import commands

from utils.embeds import info


class Help(commands.Cog):
    """Help command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="View all available commands."
    )
    async def help_command(self, interaction: discord.Interaction):

        embed = info(
            "Staff Management Commands",
            "Below is a list of all available commands."
        )

        embed.add_field(
            name="📋 General",
            value=(
                "`/help` - Shows this menu\n"
                "`/profile` - View your staff profile\n"
                "`/ping` - Check bot latency"
            ),
            inline=False
        )

        embed.add_field(
            name="🕒 Duty",
            value=(
                "`/duty` - Start your duty\n"
                "`/dutyend` - End your duty\n"
                "`/dutymanage` - Manage your active shift\n"
                "`/dutyleaderboard` - Weekly leaderboard"
            ),
            inline=False
        )

        embed.add_field(
            name="🏁 Sessions",
            value=(
                "`/sessionpanel` - Create a staff session\n"
                "`/sessionlist` - View active sessions"
            ),
            inline=False
        )

        embed.add_field(
            name="🛡 Administration",
            value=(
                "`/dutyadmin` - Manage staff shifts\n"
                "`/sessionadmin` - Manage session panels"
            ),
            inline=False
        )

        embed.set_thumbnail(
            url=interaction.guild.icon.url
            if interaction.guild and interaction.guild.icon
            else discord.Embed.Empty
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        Help(bot)
    )
