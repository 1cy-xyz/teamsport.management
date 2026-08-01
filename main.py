import os
import asyncio
import discord
from discord.ext import commands

from config import TOKEN
from database.database import setup_database
from utils.scheduler import start_scheduler

# -----------------------------
# Intents
# -----------------------------

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = False

# -----------------------------
# Bot
# -----------------------------

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# -----------------------------
# Cog Loader
# -----------------------------

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename}")

# -----------------------------
# Ready Event
# -----------------------------

@bot.event
async def on_ready():

    print("-" * 40)
    print(f"Logged in as {bot.user}")
    print(f"ID: {bot.user.id}")
    print("-" * 40)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="Staff Members"
        )
    )

    synced = await bot.tree.sync()

    print(f"Synced {len(synced)} slash commands.")

# -----------------------------
# Startup
# -----------------------------

async def main():

    async with bot:

        await setup_database()

        await load_cogs()

        start_scheduler(bot)

        await bot.start(TOKEN)

asyncio.run(main())
