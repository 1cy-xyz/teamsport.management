import discord
from datetime import datetime

from database import duty
from utils.embeds import success, error, info


class DutyView(discord.ui.View):

    def __init__(self, user_id: int):
        super().__init__(timeout=None)

        self.user_id = user_id


    # ===========================
    # Refresh Button
    # ===========================

    @discord.ui.button(
        label="Refresh",
        style=discord.ButtonStyle.primary,
        emoji="🔄"
    )
    async def refresh(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != self.user_id:

            await interaction.response.send_message(
                embed=error(
                    "Not Your Shift",
                    "You cannot manage another staff member's duty."
                ),
                ephemeral=True
            )

            return


        shift = await duty.get_active_shift(
            self.user_id
        )


        if shift is None:

            await interaction.response.send_message(
                embed=error(
                    "No Active Shift",
                    "You are not currently on duty."
                ),
                ephemeral=True
            )

            return


        start_time = datetime.fromisoformat(
            shift[1]
        )


        elapsed = datetime.utcnow() - start_time


        embed = info(
            "Current Shift",
            (
                f"🟢 Status: Active\n\n"
                f"Started:\n"
                f"<t:{int(start_time.timestamp())}:t>\n\n"
                f"Duration:\n"
                f"`{str(elapsed).split('.')[0]}`"
            )
        )


        await interaction.response.edit_message(
            embed=embed,
            view=self
        )


    # ===========================
    # End Shift Button
    # ===========================

    @discord.ui.button(
        label="End Shift",
        style=discord.ButtonStyle.danger,
        emoji="🔴"
    )
    async def end_shift(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id != self.user_id:

            await interaction.response.send_message(
                embed=error(
                    "Not Your Shift",
                    "You cannot end another staff member's shift."
                ),
                ephemeral=True
            )

            return


        duration = await duty.end_shift(
            self.user_id
        )


        if duration is None:

            await interaction.response.send_message(
                embed=error(
                    "No Active Shift",
                    "You do not have an active shift."
                ),
                ephemeral=True
            )

            return


        hours = duration // 3600
        minutes = (duration % 3600) // 60


        await interaction.response.edit_message(
            embed=success(
                "Shift Ended",
                (
                    f"Your shift has ended.\n\n"
                    f"Time Worked:\n"
                    f"`{hours}h {minutes}m`"
                )
            ),
            view=None
        )

