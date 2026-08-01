import asyncio
import aiosqlite

from datetime import datetime
from zoneinfo import ZoneInfo

from config import DATABASE, TIMEZONE
from database.duty import reset_week
from utils.embeds import info


LONDON = ZoneInfo(TIMEZONE)


class Scheduler:

    def __init__(self, bot):

        self.bot = bot
        self.last_reset = None

    async def start(self):

        await self.bot.wait_until_ready()

        while not self.bot.is_closed():

            try:

                await self.check_session_reminders()

                await self.check_weekly_reset()

            except Exception as e:

                print(f"[Scheduler] {e}")

            await asyncio.sleep(60)

    # =====================================
    # Weekly Reset
    # =====================================

    async def check_weekly_reset(self):

        now = datetime.now(LONDON)

        if (
            now.weekday() == 5
            and now.hour == 0
            and now.minute == 0
        ):

            today = now.date()

            if self.last_reset != today:

                print("Running weekly reset...")

                await reset_week()

                self.last_reset = today

                print("Weekly leaderboard reset complete.")

    # =====================================
    # Session Reminders
    # =====================================

    async def check_session_reminders(self):

        now = datetime.now(LONDON)

        current = now.strftime("%H:%M")

        async with aiosqlite.connect(DATABASE) as db:

            cursor = await db.execute("""

                SELECT

                id,
                host_name,
                track,
                session_time

                FROM sessions

            """)

            sessions = await cursor.fetchall()

            for session in sessions:

                session_id = session[0]
                host = session[1]
                track = session[2]
                session_time = session[3]

                if session_time != current:
                    continue

                reminder = await db.execute("""

                    SELECT reminder_sent

                    FROM reminders

                    WHERE session_id = ?

                """, (session_id,))

                reminder = await reminder.fetchone()

                if reminder and reminder[0] == 1:
                    continue

                cursor = await db.execute("""

                    SELECT user_id

                    FROM attendance

                    WHERE session_id = ?

                    AND attending = 1

                """, (session_id,))

                users = await cursor.fetchall()

                for user in users:

                    member = self.bot.get_user(user[0])

                    if member is None:

                        try:
                            member = await self.bot.fetch_user(user[0])
                        except Exception:
                            continue

                    try:

                        await member.send(

                            embed=info(

                                "🏁 Session Reminder",

                                (
                                    "Your staff session starts now!\n\n"

                                    f"**Host:** {host}\n"

                                    f"**Track:** {track}\n"

                                    f"**Time:** {session_time}\n\n"

                                    "Please join the server."

                                )

                            )

                        )

                    except Exception:

                        pass

                await db.execute("""

                    INSERT OR REPLACE INTO reminders

                    (
                        session_id,
                        reminder_sent
                    )

                    VALUES (?, 1)

                """, (session_id,))

                await db.commit()


def start_scheduler(bot):

    scheduler = Scheduler(bot)

    bot.loop.create_task(
        scheduler.start()
    )
