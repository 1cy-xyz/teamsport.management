import aiosqlite

from config import DATABASE


async def get_statistics():

    async with aiosqlite.connect(DATABASE) as db:

        stats = {}

        # Total Staff

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM users
        """)

        stats["staff"] = (await cursor.fetchone())[0]

        # Total Weekly Hours

        cursor = await db.execute("""
            SELECT COALESCE(SUM(weekly_seconds),0)
            FROM users
        """)

        stats["weekly"] = (await cursor.fetchone())[0]

        # Total Lifetime Hours

        cursor = await db.execute("""
            SELECT COALESCE(SUM(total_seconds),0)
            FROM users
        """)

        stats["lifetime"] = (await cursor.fetchone())[0]

        # Active Duty

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM shifts
            WHERE active = 1
        """)

        stats["active"] = (await cursor.fetchone())[0]

        # Sessions

        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM sessions
        """)

        stats["sessions"] = (await cursor.fetchone())[0]

        return stats
