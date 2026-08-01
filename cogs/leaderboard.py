import discord
from discord import app_commands
from discord.ext import commands

from database import duty
from utils.embeds import leaderboard
from config import STAFF_ROLE_ID


def format_time(seconds: int):

    hours = seconds // 3600

    minutes = (
        seconds % 3600
    ) // 60

    return f"{hours}h {minutes}m"



class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @app_commands.command(
        name="dutyleaderboard",
        description="View the weekly staff duty leaderboard."
    )
    @app_commands.checks.has_role(STAFF_ROLE_ID)
    async def duty_leaderboard(
        self,
        interaction: discord.Interaction
    ):

        if not self.is_staff(interaction.user):

            await interaction.response.send_message(
                "❌ You must have the Staff role to use this command.",
                ephemeral=True
            )
        
            return


        results = await duty.get_weekly_leaderboard(
            10
        )


        if not results:

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="🏆 Weekly Leaderboard",
                    description="No duty data found.",
                    colour=discord.Colour.gold()
                ),
                ephemeral=True
            )

            return



        embed = leaderboard(
            "Weekly Duty Leaderboard"
        )


        medals = [
            "🥇",
            "🥈",
            "🥉"
        ]


        description = ""


        position = 1


        for username, seconds in results:


            if position <= 3:

                prefix = medals[position - 1]

            else:

                prefix = f"`#{position}`"


            description += (
                f"{prefix} **{username}**\n"
                f"⏱ {format_time(seconds)}\n\n"
            )


            position += 1



        embed.description = description


        await interaction.response.send_message(
            embed=embed
        )



async def setup(bot):

    await bot.add_cog(
        Leaderboard(bot)
    )
