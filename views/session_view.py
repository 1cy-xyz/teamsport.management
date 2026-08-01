import discord

from database import sessions
from utils.embeds import success, error, info


class SessionView(discord.ui.View):

    def __init__(self, session_id: int):

        super().__init__(
            timeout=None
        )

        self.session_id = session_id



    # ==========================
    # Attend Button
    # ==========================

    @discord.ui.button(
        label="Attend",
        emoji="✅",
        style=discord.ButtonStyle.success
    )
    async def attend(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        await sessions.set_attendance(
            self.session_id,
            interaction.user.id,
            1
        )


        await interaction.response.send_message(
            embed=success(
                "Session Attendance",
                "You are now attending this session."
            ),
            ephemeral=True
        )



    # ==========================
    # Decline Button
    # ==========================

    @discord.ui.button(
        label="Decline",
        emoji="❌",
        style=discord.ButtonStyle.danger
    )
    async def decline(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        await sessions.set_attendance(
            self.session_id,
            interaction.user.id,
            0
        )


        await interaction.response.send_message(
            embed=info(
                "Session Attendance",
                "You are no longer attending this session."
            ),
            ephemeral=True
        )



    # ==========================
    # View Attendees
    # ==========================

    @discord.ui.button(
        label="View Attendees",
        emoji="👥",
        style=discord.ButtonStyle.primary
    )
    async def attendees(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):


        members = await sessions.get_attendees(
            self.session_id
        )


        if not members:

            await interaction.response.send_message(
                embed=info(
                    "Attendees",
                    "Nobody has signed up yet."
                ),
                ephemeral=True
            )

            return



        mentions = []


        for member in members:

            mentions.append(
                f"<@{member[0]}>"
            )



        await interaction.response.send_message(
            embed=info(
                "Session Attendees",
                "\n".join(mentions)
            ),
            ephemeral=True
        )
