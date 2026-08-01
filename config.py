import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# Discord
# ==========================

TOKEN = os.getenv("TOKEN")

GUILD_ID = int(os.getenv("GUILD_ID"))

ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))

SESSION_HOST_ROLE_ID = int(os.getenv("SESSION_HOST_ROLE_ID"))

LOG_CHANNEL_ID = int(os.getenb("LOG_CHANNEL_ID"))

# ==========================
# Database
# ==========================

DATABASE = "database/staff.db"

# ==========================
# Bot Settings
# ==========================

TIMEZONE = os.getenv("TIMEZONE", "Europe/London")

EMBED_COLOR = int(os.getenv("EMBED_COLOR", "0099ff"), 16)
