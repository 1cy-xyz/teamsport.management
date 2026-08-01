import aiosqlite

from config import DATABASE



async def initialise_database():

    async with aiosqlite.connect(
        DATABASE
    ) as db:


        # ==========================
        # Staff Users
        # ==========================

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users
        (

            user_id INTEGER PRIMARY KEY,

            username TEXT,

            total_seconds INTEGER DEFAULT 0,

            weekly_seconds INTEGER DEFAULT 0,

            sessions_attended INTEGER DEFAULT 0

        )
        """)



        # ==========================
        # Duty Shifts
        # ==========================

        await db.execute("""
        CREATE TABLE IF NOT EXISTS shifts
        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            start_time TEXT,

            end_time TEXT,

            duration INTEGER DEFAULT 0,

            active INTEGER DEFAULT 0

        )
        """)



        # ==========================
        # Sessions
        # ==========================

        await db.execute("""
        CREATE TABLE IF NOT EXISTS sessions
        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            message_id INTEGER,

            channel_id INTEGER,

            guild_id INTEGER,

            host_id INTEGER,

            host_name TEXT,

            track TEXT,

            session_time TEXT,

            created_at TEXT

        )
        """)



        # ==========================
        # Session Attendance
        # ==========================

        await db.execute("""
        CREATE TABLE IF NOT EXISTS attendance
        (

            session_id INTEGER,

            user_id INTEGER,

            attending INTEGER DEFAULT 0,

            PRIMARY KEY
            (
                session_id,
                user_id
            )

        )
        """)



        # ==========================
        # Reminder Tracking
        # ==========================

        await db.execute("""
        CREATE TABLE IF NOT EXISTS reminders
        (

            session_id INTEGER PRIMARY KEY,

            reminder_sent INTEGER DEFAULT 0

        )
        """)



        # ==========================
        # Bot Settings
        # ==========================

        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings
        (

            setting TEXT PRIMARY KEY,

            value TEXT

        )
        """)



        await db.commit()



    print(
        "Database initialised successfully."
    )
