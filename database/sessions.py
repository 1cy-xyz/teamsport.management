import aiosqlite

from config import DATABASE


# ==========================
# Create Session
# ==========================

async def create_session(
    message_id: int,
    channel_id: int,
    guild_id: int,
    host_id: int,
    host_name: str,
    track: str,
    session_time: str,
    created_at: str
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            INSERT INTO sessions
            (
                message_id,
                channel_id,
                guild_id,
                host_id,
                host_name,
                track,
                session_time,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        """,
        (
            message_id,
            channel_id,
            guild_id,
            host_id,
            host_name,
            track,
            session_time,
            created_at
        ))

        await db.commit()

        return cursor.lastrowid



# ==========================
# Attendance
# ==========================

async def set_attendance(
    session_id: int,
    user_id: int,
    attending: int
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            INSERT INTO attendance
            (
                session_id,
                user_id,
                attending
            )

            VALUES (?, ?, ?)

            ON CONFLICT(session_id,user_id)

            DO UPDATE SET

            attending = excluded.attending

        """,
        (
            session_id,
            user_id,
            attending
        ))

        await db.commit()



# ==========================
# Get Attendees
# ==========================

async def get_attendees(
    session_id: int
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT user_id

            FROM attendance

            WHERE session_id = ?

            AND attending = 1

        """,
        (
            session_id,
        ))

        return await cursor.fetchall()



# ==========================
# Get Session
# ==========================

async def get_session_by_message(
    message_id: int
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT *

            FROM sessions

            WHERE message_id = ?

        """,
        (
            message_id,
        ))

        return await cursor.fetchone()
