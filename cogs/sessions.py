import discord

from discord import app_commands
from discord.ext import commands

from datetime import datetime

from config import SESSION_HOST_ROLE_ID

from database import sessions

from views.session_view import SessionView

from utils.embeds import (
    session,
    error,
    success
)


class Sessions(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    def has_permission(
        self,
        interaction: discord.Interaction
    ):

        return any(
            role.id == SESSION_HOST_ROLE_ID
            for role in interaction.user.roles
        )



    # ==========================
    # SESSION PANEL
    # ==========================


    @app_commands.command(
        name="sessionpanel",
        description="Create a staff session panel."
    )
    @app_commands.describe(
        host="The person hosting the session",
        time="The session start time",
        track="The track/location"
    )
    async def session_panel(
        self,
        interaction: discord.Interaction,
        host: discord.Member,
        time: str,
        track: str
    ):


        if not self.has_permission(interaction):

            await interaction.response.send_message(
                embed=error(
                    "Permission Denied",
                    "You cannot create sessions."
                ),
                ephemeral=True
            )

            return



        embed = session(
            "Staff Session",
            host=host.mention,
            track=track,
            time=time
        )


        await interaction.response.send_message(
            embed=embed
        )


        message = await interaction.original_response()



        session_id = await sessions.create_session(

            message_id=message.id,

            channel_id=interaction.channel.id,

            guild_id=interaction.guild.id,

            host_id=host.id,

            host_name=str(host),

            track=track,

            session_time=time,

            created_at=datetime.utcnow().isoformat()

        )



        await message.edit(
            view=SessionView(
                session_id
            )
        )


        await interaction.followup.send(
            embed=success(
                "Session Created",
                "The session panel has been created."
            ),
            ephemeral=True
        )



async def setup(bot):

    await bot.add_cog(
        Sessions(bot)
    )
