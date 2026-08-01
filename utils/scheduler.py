import asyncio
from datetime import datetime, timedelta

import discord
import pytz

from config import TIMEZONE

from database import duty
from database import sessions



timezone = pytz.timezone(
    TIMEZONE
)



# ==========================
# Weekly Reset Checker
# ==========================

async def weekly_reset():

    while True:

        now = datetime.now(
            timezone
        )


        # Saturday 00:00

        if (
            now.weekday() == 5
            and now.hour == 0
            and now.minute == 0
        ):

            await duty.reset_week()


            print(
                "Weekly duty reset completed."
            )


            # Wait an hour so it
            # doesn't run repeatedly

            await asyncio.sleep(
                3600
            )


        await asyncio.sleep(
            60
        )



# ==========================
# Session Reminder System
# ==========================

async def session_reminders(
    bot
):

    while True:

        now = datetime.now(
            timezone
        )


        # Get upcoming sessions

        async with sessions.get_database() as db:

            cursor = await db.execute("""
                SELECT *

                FROM sessions

            """)


            session_list = await cursor.fetchall()



        for session in session_list:


            try:

                session_id = session[0]

                session_time = datetime.fromisoformat(
                    session[7]
                )


                session_time = timezone.localize(
                    session_time
                )


                difference = (
                    session_time - now
                )



                # Send reminder 30 minutes before

                if (
                    timedelta(minutes=29)
                    <
                    difference
                    <
                    timedelta(minutes=31)
                ):


                    already_sent = await sessions.reminder_sent(
                        session_id
                    )


                    if not already_sent:


                        attendees = await sessions.get_attendees(
                            session_id
                        )


                        for user in attendees:


                            member = bot.get_user(
                                user[0]
                            )


                            if member:


                                embed = discord.Embed(

                                    title="🏁 Session Reminder",

                                    description=(

                                        "Your session starts in **30 minutes**.\n\n"

                                        f"Track: **{session[6]}**\n"

                                        f"Host: <@{session[4]}>"

                                    ),

                                    colour=discord.Colour.blue()

                                )


                                await member.send(
                                    embed=embed
                                )


                        await sessions.mark_reminder_sent(
                            session_id
                        )


            except Exception as e:

                print(
                    f"Reminder error: {e}"
                )



        await asyncio.sleep(
            60
        )



# ==========================
# Start Scheduler
# ==========================

def start_scheduler(
    bot
):

    asyncio.create_task(
        weekly_reset()
    )


    asyncio.create_task(
        session_reminders(
            bot
        )
    )


    print(
        "Scheduler started."
    )
