import discord

from discord import app_commands
from discord.ext import commands

from config import ADMIN_ROLE_ID

from database import session_admin

from utils.embeds import (
    success,
    error,
    info
)


class SessionAdmin(
    commands.GroupCog,
    name="sessionadmin"
):


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



    # ==========================
    # DELETE
    # ==========================

    @app_commands.command(
        name="delete",
        description="Delete a session."
    )
    async def delete(
        self,
        interaction: discord.Interaction,
        session_id: int
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied"
                ),
                ephemeral=True
            )

            return


        await session_admin.delete_session(
            session_id
        )


        await interaction.response.send_message(
            embed=success(
                "Session Deleted",
                f"Deleted session #{session_id}"
            )
        )



    # ==========================
    # CLOSE
    # ==========================

    @app_commands.command(
        name="close",
        description="Close session signups."
    )
    async def close(
        self,
        interaction: discord.Interaction,
        session_id: int
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied"
                ),
                ephemeral=True
            )

            return



        await session_admin.close_session(
            session_id
        )


        await interaction.response.send_message(
            embed=success(
                "Session Closed",
                "Staff can no longer sign up."
            )
        )



    # ==========================
    # ATTENDEES
    # ==========================

    @app_commands.command(
        name="attendees",
        description="View session attendees."
    )
    async def attendees(
        self,
        interaction: discord.Interaction,
        session_id: int
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied"
                ),
                ephemeral=True
            )

            return



        users = await session_admin.get_session_attendance(
            session_id
        )


        attending = []


        for user,status in users:

            if status == 1:

                attending.append(
                    f"<@{user}>"
                )


        await interaction.response.send_message(
            embed=info(
                "Session Attendees",
                "\n".join(attending)
                if attending
                else "Nobody attending."
            )
        )



    # ==========================
    # FORCE ADD
    # ==========================

    @app_commands.command(
        name="forceadd",
        description="Force a user into a session."
    )
    async def forceadd(
        self,
        interaction: discord.Interaction,
        session_id: int,
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



        await session_admin.force_attendance(
            session_id,
            member.id,
            1
        )


        await interaction.response.send_message(
            embed=success(
                "Added",
                f"{member.mention} added."
            )
        )



async def setup(bot):

    await bot.add_cog(
        SessionAdmin(bot)
    )
