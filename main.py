# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import discord
from discord.ext import commands
from config import BOT_TOKEN

bot = commands.Bot(command_prefix="!")

@bot.command()
async def hello(context)
    await context.reply("Hello!")

bot.run(BOT_TOKEN)

