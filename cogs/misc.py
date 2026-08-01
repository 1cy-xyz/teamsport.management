import discord
import time

from discord import app_commands
from discord.ext import commands

from utils.embeds import info


class Misc(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.start_time = time.time()


    # ==========================
    # PING
    # ==========================

    @app_commands.command(
        name="ping",
        description="View the bot latency."
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):

        latency = round(
            self.bot.latency * 1000
        )

        embed = info(
            "Bot Ping",
            f"🏓 Latency: `{latency}ms`"
        )

        await interaction.response.send_message(
            embed=embed
        )


    # ==========================
    # BOT INFO
    # ==========================

    @app_commands.command(
        name="botinfo",
        description="View information about the bot."
    )
    async def botinfo(
        self,
        interaction: discord.Interaction
    ):

        guilds = len(self.bot.guilds)

        users = len(self.bot.users)

        embed = info(
            "Staff Management Bot"
        )

        embed.add_field(
            name="Servers",
            value=str(guilds),
            inline=True
        )

        embed.add_field(
            name="Users",
            value=str(users),
            inline=True
        )

        embed.add_field(
            name="Library",
            value="discord.py 2.x",
            inline=True
        )

        embed.add_field(
            name="Developer",
            value="Your Staff Team",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )


    # ==========================
    # UPTIME
    # ==========================

    @app_commands.command(
        name="uptime",
        description="View bot uptime."
    )
    async def uptime(
        self,
        interaction: discord.Interaction
    ):

        uptime_seconds = int(
            time.time() - self.start_time
        )

        days = uptime_seconds // 86400

        hours = (
            uptime_seconds % 86400
        ) // 3600

        minutes = (
            uptime_seconds % 3600
        ) // 60

        embed = info(
            "Bot Uptime",
            f"⏱ {days}d {hours}h {minutes}m"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Misc(bot)
    )
