import discord
from discord.ext import tasks
import os
import re
import logger
from typing import Callable, Awaitable

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("DISCORD_TOKEN missing from env vars")
GUILD_ID = 706426037415837698
ANKUR_NAME = "the kid#7020"

_client = None

def connect(run_loop: Callable[[], Awaitable[None]], cooldown: int):
    global _client
    intents = discord.Intents.default()
    intents.members = True

    class MyClient(discord.Client):
        async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            self.run_app.start()

        @tasks.loop(seconds=cooldown)  # task runs every 60 seconds
        async def run_app(self):
            await run_loop()

        @run_app.before_loop
        async def before_run_app(self):
            await self.wait_until_ready()

    _client = MyClient(intents=intents)
    _client.run(TOKEN)

async def change_name(champion: str, rank: str, division: str):
    assert _client, "Client no longer exists"
    monarcho_guild = [
        guild for guild in _client.guilds if guild.id == GUILD_ID
    ][0]

    ankur_member = monarcho_guild.get_member_named(ANKUR_NAME)
    ankur_display_name = ankur_member.display_name
    logger.log(f"Ankur's current Discord name: {ankur_display_name}")
