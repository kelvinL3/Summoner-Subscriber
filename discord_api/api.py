import discord
from discord.ext import tasks
import os
import re
import logger
from typing import Callable, Awaitable, Optional

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("DISCORD_TOKEN missing from env vars")
GUILD_ID = 706426037415837698

_client: Optional[discord.Client] = None


def connect(run_loop: Callable[[], Awaitable[None]], cooldown: int) -> None:
    global _client
    intents = discord.Intents.default()
    intents.members = True

    class MyClient(discord.Client):
        async def on_ready(self):
            print(f"Logged in as {self.user} (ID: {self.user.id})")
            self.run_app.start()

        @tasks.loop(seconds=cooldown)  # task runs every 60 seconds
        async def run_app(self):
            await run_loop()

        @run_app.before_loop
        async def before_run_app(self):
            await self.wait_until_ready()

    _client = MyClient(intents=intents)
    _client.run(TOKEN)


async def change_name(disc_handle: str, champion: str, rank: str, division: str) -> None:
    assert _client, "Client no longer exists"
    monarcho_guild = [guild for guild in _client.guilds if guild.id == GUILD_ID][0]

    ankur_member = monarcho_guild.get_member_named(disc_handle)
    ankur_display_name = ankur_member.display_name
    logger.log(f"Ankur's current Discord name: {ankur_display_name}")

    ankurs_new_name = f"{champion} - {rank} {division}"
    if ankur_display_name != ankurs_new_name:
        logger.log(f"Updating ankur's discord name to {ankurs_new_name}")
        db.update_discord_name(disc_handle, ankur_display_name)
        await ankur_member.edit(nick=ankurs_new_name)

async def revert_name(disc_handle: str) -> None:
    # TODO - use account ID instead of handle since
    # ankur can change his handle
    ankurs_old_name = db.get_discord_name(disc_handle)
    logger.log(f"Reverting ankur's discord name to {ankurs_old_name}")
    await ankur_member.edit(nick=ankurs_old_name)
