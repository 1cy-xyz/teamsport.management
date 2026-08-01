import discord
import os
import asyncio

from discord.ext import commands

from config import TOKEN

from utils.scheduler import start_scheduler

from database.database import initialise_database

from utils.webserver import keep_alive


# ==========================
# Bot Configuration
# ==========================

intents = discord.Intents.default()

intents.members = True
intents.message_content = True
intents.presences = True


class StaffBot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=intents
        )


    async def setup_hook(self):

        print("Starting database...")

        await initialise_database()


        print("Loading cogs...")


        for filename in os.listdir("./cogs"):

            if filename.endswith(".py"):

                try:

                    await self.load_extension(
                        f"cogs.{filename[:-3]}"
                    )

                    print(
                        f"Loaded {filename}"
                    )

                except Exception as e:

                    print(
                        f"Failed loading {filename}: {e}"
                    )


        print("Syncing commands...")


        try:
            from config import GUILD_ID
            
            guild = discord.Object(
                id=GUILD_ID
            )
            
            synced = await self.tree.sync(
                guild=guild
            )

            print(
                f"Synced {len(synced)} commands"
            )

        except Exception as e:

            print(
                f"Command sync failed: {e}"
            )


        print("Starting scheduler...")

        start_scheduler(
            self
        )



    async def on_ready(self):

        print("--------------------------------")
        print(
            f"Logged in as {self.user}"
        )
        print(
            f"Bot ID: {self.user.id}"
        )
        print(
            f"Servers: {len(self.guilds)}"
        )
        print("--------------------------------")



    async def on_command_error(
        self,
        ctx,
        error
    ):

        print(
            f"Command error: {error}"
        )



# ==========================
# Start Bot
# ==========================


bot = StaffBot()


async def main():

    async with bot:

        await bot.start(
            TOKEN
        )


if __name__ == "__main__":

    keep_alive()

    asyncio.run(
        main()
    )
