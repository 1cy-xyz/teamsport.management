import discord

from config import LOG_CHANNEL_ID


async def send_log(
    bot,
    title,
    description,
    colour=discord.Colour.blue()
):

    channel = bot.get_channel(
        LOG_CHANNEL_ID
    )


    if channel is None:
        return


    embed = discord.Embed(
        title=title,
        description=description,
        colour=colour,
        timestamp=discord.utils.utcnow()
    )


    await channel.send(
        embed=embed
    )
