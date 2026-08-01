import discord
from discord import app_commands
from discord.ext import commands

from database import duty
from views.duty_view import DutyView
from utils.embeds import success, error, info
from utils.logger import send_log
from config import STAFF_ROLE_ID

def is_staff(self, member: discord.Member):

    return any(
        role.id == STAFF_ROLE_ID
        for role in member.roles
    )


class Duty(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # ==========================
    # Start Duty
    # ==========================

    @app_commands.command(
        name="duty",
        description="Start your staff duty shift."
    )
    async def duty_start(
        self,
        interaction: discord.Interaction
    ):

        if not self.is_staff(interaction.user):

            await interaction.response.send_message(
                "❌ You must have the Staff role to use this command.",
                ephemeral=True
            )
        
            return
        user = interaction.user


        await duty.create_user(
            user.id,
            user.name
        )


        active = await duty.get_active_shift(
            user.id
        )


        if active:

            await interaction.response.send_message(
                embed=error(
                    "Already On Duty",
                    "You already have an active shift."
                ),
                ephemeral=True
            )

            return


        await duty.start_shift(
            user.id
        )

        await send_log(
            self.bot,
            "🟢 Duty Started",
            f"{user.mention} started their shift.",
            discord.Colour.green()
        )


        await interaction.response.send_message(
            embed=success(
                "Shift Started",
                (
                    f"{user.mention} has started their shift.\n\n"
                    "Use `/dutymanage` to manage your shift."
                )
            )
        )



    # ==========================
    # End Duty
    # ==========================

    @app_commands.command(
        name="dutyend",
        description="End your current staff shift."
    )
    async def duty_end(
        self,
        interaction: discord.Interaction
    ):

        if not self.is_staff(interaction.user):

            await interaction.response.send_message(
                "❌ You must have the Staff role to use this command.",
                ephemeral=True
            )
        
            return
        duration = await duty.end_shift(
            interaction.user.id
        )

        await send_log(
            self.bot,
            "🔴 Duty Ended",
            (
                f"{interaction.user.mention} ended their shift.\n"
                f"Duration: `{hours}h {minutes}m`"
            ),
            discord.Colour.red()
        )


        if duration is None:

            await interaction.response.send_message(
                embed=error(
                    "No Active Shift",
                    "You are not currently on duty."
                ),
                ephemeral=True
            )

            return



        hours = duration // 3600

        minutes = (
            duration % 3600
        ) // 60



        await interaction.response.send_message(
            embed=success(
                "Shift Ended",
                (
                    f"Your shift has ended.\n\n"
                    f"Time Worked:\n"
                    f"`{hours}h {minutes}m`"
                )
            )
        )



    # ==========================
    # Duty Management Panel
    # ==========================

    @app_commands.command(
        name="dutymanage",
        description="Manage your current shift."
    )
    async def duty_manage(
        self,
        interaction: discord.Interaction
    ):

        if not self.is_staff(interaction.user):

            await interaction.response.send_message(
                "❌ You must have the Staff role to use this command.",
                ephemeral=True
            )
        
            return

        shift = await duty.get_active_shift(
            interaction.user.id
        )


        if shift is None:

            await interaction.response.send_message(
                embed=error(
                    "No Active Shift",
                    "Start a shift first using `/duty`."
                ),
                ephemeral=True
            )

            return



        await interaction.response.send_message(
            embed=info(
                "Current Shift",
                (
                    "🟢 You are currently on duty.\n\n"
                    "Use the buttons below to manage your shift."
                )
            ),
            view=DutyView(
                interaction.user.id
            ),
            ephemeral=True
        )



async def setup(bot):

    await bot.add_cog(
        Duty(bot)
    )
