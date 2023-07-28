# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import discord
import syllapy
from discord.ext import commands
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def is_haiku(text):
    lines = text.splitlines()
    if len(lines) != 3:
        return False
    return syllapy.count(lines[0]) == 5 and syllapy.count(lines[1]) == 7 and syllapy.count(lines[2]) == 6


@bot.command()
async def frenchfry(context):
    await context.reply("I love French Fry!")

@bot.command()
async def hello(context):
    await context.reply("Hello!")


@bot.command()
async def count(context, *args):
    arguments = " ".join(args)
    await context.reply(f'{arguments} has {syllapy.count(arguments)} syllables.')


@bot.event
async def on_message(message):
    # Ignore messages from the bot
    if message.author == bot.user:
        return

    content = message.content
    if is_haiku(content):
        await message.channel.send(f"Detected a Haiku from {message.author.mention}:\n{content}")

    await bot.process_commands(message)  # to allow processing commands in addition to the on_message event


bot.run(BOT_TOKEN)
