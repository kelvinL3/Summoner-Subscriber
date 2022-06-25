import discord
import os
import re
import logger


TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("DISCORD_TOKEN missing from env vars")

GUILD_ID = 706426037415837698
ANKUR_NAME = "the kid#7020"

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

async def connect():
    await client.start(TOKEN)
    print("Connected")


async def change_name(champion: str, rank: str, division: str):
    print(client.guilds)
    monarcho_guild = [
        guild for guild in client.guilds if guild.id == GUILD_ID
    ][0]

    ankur_member = monarcho_guild.get_member_named(ANKUR_NAME)
    ankur_display_name = ankur_member.display_name
    logger.log(f"Ankur's current Discord name: {ankur_display_name}")

    # reg = re.search("(.+)-\s*(\d+games\s+\w+)", ankur_display_name)

    # await ankur_member.edit(nick=ankur_display_name + ";")
    # try:
    # normal, status = reg.groups()
    # await ankur_member.edit(nick=f"{normal} - {rank} {division}")
    # except :
    #     raise
