import aiosqlite

from config import DATABASE


def get_database():

    return aiosqlite.connect(
        DATABASE
    )

# ==========================
# Create Session
# ==========================

async def create_session(
    message_id,
    channel_id,
    guild_id,
    host_id,
    host_name,
    track,
    session_time,
    created_at
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
# Get Session
# ==========================

async def get_session(
    session_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT *

            FROM sessions

            WHERE id = ?

        """,
        (
            session_id,
        ))


        return await cursor.fetchone()



# ==========================
# Get By Message ID
# ==========================

async def get_session_by_message(
    message_id
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



# ==========================
# Attendance Update
# ==========================

async def set_attendance(
    session_id,
    user_id,
    attending
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
    session_id
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
# Get Declines
# ==========================

async def get_declines(
    session_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT user_id

            FROM attendance

            WHERE session_id = ?

            AND attending = 0

        """,
        (
            session_id,
        ))


        return await cursor.fetchall()



# ==========================
# Attendance Counts
# ==========================

async def get_attendance_count(
    session_id
):

    async with aiosqlite.connect(DATABASE) as db:


        cursor = await db.execute("""
            SELECT

            SUM(
                CASE WHEN attending = 1
                THEN 1 ELSE 0 END
            ),

            SUM(
                CASE WHEN attending = 0
                THEN 1 ELSE 0 END
            )


            FROM attendance

            WHERE session_id = ?

        """,
        (
            session_id,
        ))


        result = await cursor.fetchone()


        attending = result[0] or 0

        declined = result[1] or 0


        return attending, declined



# ==========================
# Force Add
# ==========================

async def force_add(
    session_id,
    user_id
):

    await set_attendance(
        session_id,
        user_id,
        1
    )



# ==========================
# Remove Attendance
# ==========================

async def remove_attendance(
    session_id,
    user_id
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            DELETE FROM attendance

            WHERE session_id = ?

            AND user_id = ?

        """,
        (
            session_id,
            user_id
        ))


        await db.commit()



# ==========================
# Reminder Check
# ==========================

async def reminder_sent(
    session_id
):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
            SELECT reminder_sent

            FROM reminders

            WHERE session_id = ?

        """,
        (
            session_id,
        ))


        result = await cursor.fetchone()


        if result:

            return result[0] == 1


        return False



async def mark_reminder_sent(
    session_id
):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
            INSERT OR REPLACE INTO reminders

            (
                session_id,
                reminder_sent
            )

            VALUES (?,1)

        """,
        (
            session_id,
        ))


        await db.commit()
