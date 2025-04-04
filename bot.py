import discord
import config
from tracker import StatusTracker

intents = discord.Intents.default()
intents.members = True

bot = StatusTracker(intents=intents)

bot.run(config.TOKEN)
