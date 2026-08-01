import discord

from discord import app_commands
from discord.ext import commands

from config import ADMIN_ROLE_ID

from database import duty

from utils.embeds import (
    success,
    error,
    info
)

from utils.logger import send_log


class DutyAdmin(commands.GroupCog, name="dutyadmin"):

    def __init__(self, bot):

        self.bot = bot



    def has_permission(
        self,
        interaction
    ):

        return any(
            role.id == ADMIN_ROLE_ID
            for role in interaction.user.roles
        )



    # ===========================
    # CREATE SHIFT
    # ===========================


    @app_commands.command(
        name="create",
        description="Create a manual staff shift."
    )
    async def create(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        hours: int
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied",
                    "You cannot use this command."
                ),
                ephemeral=True
            )

            return



        seconds = hours * 3600


        await duty.admin_create_shift(
            member.id,
            seconds
        )

        await send_log(
            self.bot,
            "🛠 Shift Created",
            (
                f"Admin: {interaction.user.mention}\n"
                f"Staff: {member.mention}\n"
                f"Duration: {hours}h"
            ),
            discord.Colour.orange()
        )



        await interaction.response.send_message(
            embed=success(
                "Shift Created",
                (
                    f"Created a {hours} hour shift "
                    f"for {member.mention}"
                )
            )
        )



    # ===========================
    # DELETE SHIFT
    # ===========================


    @app_commands.command(
        name="delete",
        description="Delete a shift by ID."
    )
    async def delete(
        self,
        interaction: discord.Interaction,
        shift_id: int
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied"
                ),
                ephemeral=True
            )

            return



        await duty.admin_delete_shift(
            shift_id
        )


        await interaction.response.send_message(
            embed=success(
                "Shift Deleted",
                f"Deleted shift #{shift_id}"
            )
        )



    # ===========================
    # RESET USER
    # ===========================


    @app_commands.command(
        name="reset",
        description="Reset a member's weekly hours."
    )
    async def reset(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied"
                ),
                ephemeral=True
            )

            return



        await duty.admin_reset_user(
            member.id
        )


        await interaction.response.send_message(
            embed=success(
                "Hours Reset",
                f"Reset weekly hours for {member.mention}"
            )
        )



    # ===========================
    # VIEW HISTORY
    # ===========================


    @app_commands.command(
        name="history",
        description="View a staff member's shifts."
    )
    async def history(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied"
                ),
                ephemeral=True
            )

            return



        shifts = await duty.admin_get_shifts(
            member.id
        )


        text = ""


        for shift in shifts[:10]:

            text += (
                f"#{shift[0]} - "
                f"{shift[1]//3600}h\n"
            )


        await interaction.response.send_message(
            embed=info(
                f"{member.name}'s History",
                text or "No shifts found."
            )
        )



async def setup(bot):

    await bot.add_cog(
        DutyAdmin(bot)
    )
