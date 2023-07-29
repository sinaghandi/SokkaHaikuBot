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


def count_sentence(sentence):
    syllables = 0
    words = sentence.split()
    for word in words:
        syllables += syllapy.count(word)
    return syllables


def is_haiku(text):
    words = text.split()
    syllables_list = []
    for word in words:
        syllables = syllapy.count(word)
        syllables_list.append((word, syllables))
    if sum(word[1] for word in syllables_list) != 18:
        return False

    syllables_current = 0
    line1 = []
    line2 = []
    line3 = []

    for syllables in syllables_list:
        line1.append(syllables[0])
        syllables_current += syllables[1]
        if syllables_current > 5:
            return False
        if syllables_current == 5:
            syllables_list = syllables_list[syllables_list.index(syllables) + 1:]
            break

    syllables_current = 0
    for syllables in syllables_list:
        line2.append(syllables[0])
        syllables_current += syllables[1]
        if syllables_current > 7:
            return False
        if syllables_current == 7:
            syllables_list = syllables_list[syllables_list.index(syllables) + 1:]
            break

    for syllables in syllables_list:
        line3.append(syllables[0])
        syllables_current += syllables[1]

    return [True, [line1, line2, line3]]


@bot.command()
async def frenchfry(context):
    await context.reply("I love French Fry!")


@bot.command()
async def hello(context):
    await context.reply("Hello!")


@bot.command()
async def count(context, *args):
    arguments = " ".join(args)
    await context.reply(f'{arguments} has {count_sentence(arguments)} syllables.')


@bot.event
async def on_message(message):
    # Ignore messages from the bot
    if message.author == bot.user:
        return

    content = message.content
    haiku = is_haiku(content)
    if haiku:
        line1 = " ".join(haiku[1][0])
        line2 = " ".join(haiku[1][1])
        line3 = " ".join(haiku[1][2])
        await message.channel.send(f"\n{line1}\n{line2}\n{line3}")

    await bot.process_commands(message)  # to allow processing commands in addition to the on_message event


bot.run(BOT_TOKEN)
