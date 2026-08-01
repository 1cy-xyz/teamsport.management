import aiosqlite

from config import DATABASE


# ==========================
# Delete Session
# ==========================

async def delete_session(
    session_id: int
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            DELETE FROM attendance

            WHERE session_id = ?

        """,
        (
            session_id,
        ))


        await db.execute("""
            DELETE FROM reminders

            WHERE session_id = ?

        """,
        (
            session_id,
        ))


        await db.execute("""
            DELETE FROM sessions

            WHERE id = ?

        """,
        (
            session_id,
        ))


        await db.commit()



# ==========================
# Close Session
# ==========================

async def close_session(
    session_id: int
):

    async with aiosqlite.connect(DATABASE) as db:


        await db.execute("""
            UPDATE sessions

            SET

            session_time = 'CLOSED'

            WHERE id = ?

        """,
        (
            session_id,
        ))


        await db.commit()



# ==========================
# Get Attendance
# ==========================

async def get_session_attendance(
    session_id: int
):

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
            SELECT

            user_id,
            attending

            FROM attendance

            WHERE session_id = ?

        """,
        (
            session_id,
        ))


        return await cursor.fetchall()



# ==========================
# Force Attendance Change
# ==========================

async def force_attendance(
    session_id: int,
    user_id: int,
    status: int
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
            status
        ))


        await db.commit()
