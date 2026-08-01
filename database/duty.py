import aiosqlite

from datetime import datetime

from config import DATABASE



# ==========================
# Create User
# ==========================

async def create_user(
    user_id,
    username
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            INSERT OR IGNORE INTO users
            (
                user_id,
                username
            )

            VALUES (?, ?)

        """,
        (
            user_id,
            username
        ))

        await db.commit()



# ==========================
# Start Shift
# ==========================

async def start_shift(
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            INSERT INTO shifts
            (
                user_id,
                start_time,
                active
            )

            VALUES (?, ?, 1)

        """,
        (
            user_id,
            datetime.utcnow().isoformat()
        ))

        await db.commit()



# ==========================
# Get Active Shift
# ==========================

async def get_active_shift(
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT *

            FROM shifts

            WHERE user_id = ?

            AND active = 1

        """,
        (
            user_id,
        ))

        return await cursor.fetchone()



# ==========================
# End Shift
# ==========================

async def end_shift(
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT id,start_time

            FROM shifts

            WHERE user_id = ?

            AND active = 1

        """,
        (
            user_id,
        ))

        shift = await cursor.fetchone()


        if shift is None:

            return None



        start = datetime.fromisoformat(
            shift[1]
        )


        end = datetime.utcnow()


        duration = int(
            (end - start).total_seconds()
        )



        await db.execute("""
            UPDATE shifts

            SET

            end_time = ?,

            duration = ?,

            active = 0

            WHERE id = ?

        """,
        (
            end.isoformat(),
            duration,
            shift[0]
        ))



        await db.execute("""
            UPDATE users

            SET

            total_seconds =
            total_seconds + ?,

            weekly_seconds =
            weekly_seconds + ?

            WHERE user_id = ?

        """,
        (
            duration,
            duration,
            user_id
        ))



        await db.commit()


        return duration



# ==========================
# Weekly Leaderboard
# ==========================

async def get_weekly_leaderboard(
    limit=10
):

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
            SELECT

            username,

            weekly_seconds

            FROM users

            ORDER BY weekly_seconds DESC

            LIMIT ?

        """,
        (
            limit,
        ))


        return await cursor.fetchall()



# ==========================
# Reset Weekly Hours
# ==========================

async def reset_week():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            UPDATE users

            SET weekly_seconds = 0

        """)

        await db.commit()



# ==========================
# Profile
# ==========================

async def get_profile(
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT

            username,

            total_seconds,

            weekly_seconds,

            sessions_attended

            FROM users

            WHERE user_id = ?

        """,
        (
            user_id,
        ))


        return await cursor.fetchone()



# ==========================
# Add Session Attendance
# ==========================

async def add_session_attendance(
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            UPDATE users

            SET sessions_attended =
            sessions_attended + 1

            WHERE user_id = ?

        """,
        (
            user_id,
        ))

        await db.commit()



# ==========================
# Get All Staff
# ==========================

async def get_all_staff():

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT *

            FROM users

        """)

        return await cursor.fetchall()



# ==========================
# Admin Create Shift
# ==========================

async def admin_create_shift(
    user_id,
    duration
):

    async with aiosqlite.connect(DATABASE) as db:


        now = datetime.utcnow()


        await db.execute("""
            INSERT INTO shifts

            (
                user_id,
                start_time,
                end_time,
                duration
            )

            VALUES (?, ?, ?, ?)

        """,
        (
            user_id,
            now.isoformat(),
            now.isoformat(),
            duration
        ))


        await db.execute("""
            UPDATE users

            SET

            total_seconds =
            total_seconds + ?,

            weekly_seconds =
            weekly_seconds + ?

            WHERE user_id = ?

        """,
        (
            duration,
            duration,
            user_id
        ))


        await db.commit()



# ==========================
# Admin Delete Shift
# ==========================

async def admin_delete_shift(
    shift_id
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            DELETE FROM shifts

            WHERE id = ?

        """,
        (
            shift_id,
        ))

        await db.commit()



# ==========================
# Admin Reset User
# ==========================

async def admin_reset_user(
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            UPDATE users

            SET weekly_seconds = 0

            WHERE user_id = ?

        """,
        (
            user_id,
        ))

        await db.commit()



# ==========================
# Admin History
# ==========================

async def admin_get_shifts(
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT

            id,
            duration,
            start_time

            FROM shifts

            WHERE user_id = ?

            ORDER BY id DESC

        """,
        (
            user_id,
        ))


        return await cursor.fetchall()
