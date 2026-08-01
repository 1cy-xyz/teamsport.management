import aiosqlite

from config import DATABASE



# ==========================
# Get Full Statistics
# ==========================

async def get_statistics():

    async with aiosqlite.connect(DATABASE) as db:

        stats = {}


        # Total registered staff

        cursor = await db.execute("""
            SELECT COUNT(*)

            FROM users

        """)

        stats["staff"] = (
            await cursor.fetchone()
        )[0]



        # Staff currently on duty

        cursor = await db.execute("""
            SELECT COUNT(*)

            FROM shifts

            WHERE active = 1

        """)

        stats["active"] = (
            await cursor.fetchone()
        )[0]



        # Weekly hours

        cursor = await db.execute("""
            SELECT COALESCE(
                SUM(weekly_seconds),
                0
            )

            FROM users

        """)

        stats["weekly"] = (
            await cursor.fetchone()
        )[0]



        # Lifetime hours

        cursor = await db.execute("""
            SELECT COALESCE(
                SUM(total_seconds),
                0
            )

            FROM users

        """)

        stats["lifetime"] = (
            await cursor.fetchone()
        )[0]



        # Sessions created

        cursor = await db.execute("""
            SELECT COUNT(*)

            FROM sessions

        """)

        stats["sessions"] = (
            await cursor.fetchone()
        )[0]



        # Average lifetime hours

        if stats["staff"] > 0:

            stats["average"] = (
                stats["lifetime"]
                //
                stats["staff"]
            )

        else:

            stats["average"] = 0



        return stats



# ==========================
# Top Staff
# ==========================

async def get_top_staff(
    limit=10
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT

            username,

            total_seconds

            FROM users

            ORDER BY total_seconds DESC

            LIMIT ?

        """,
        (
            limit,
        ))


        return await cursor.fetchall()



# ==========================
# Session Statistics
# ==========================

async def get_session_statistics():

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT COUNT(*)

            FROM attendance

            WHERE attending = 1

        """)

        attendees = (
            await cursor.fetchone()
        )[0]


        cursor = await db.execute("""
            SELECT COUNT(*)

            FROM sessions

        """)

        sessions = (
            await cursor.fetchone()
        )[0]


        return {
            "attendees": attendees,
            "sessions": sessions
        }
