import discord
import syllapy
from discord.ext import commands
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def is_haiku(text):
    """Determines if the provided text forms a 5-7-6 haiku.

    Args:
        text (str): The text to be checked.

    Returns:
        Tuple[bool, List[List[str]]]: A tuple containing a boolean indicating if the text is a haiku,
        and a list of the three lines if it is.
    """
    words = text.split()
    syllables_list = []
    # Checks if total syllables in text equals 18
    for word in words:
        syllables = syllapy.count(word)
        syllables_list.append((word, syllables))
    if sum(word[1] for word in syllables_list) != 18:
        return False

    syllables_current = 0
    # will be filled with respective lines of the haiku
    line1 = []
    line2 = []
    line3 = []

    # Checks if there is a break at 5 total syllables to form first line
    for syllables in syllables_list:
        line1.append(syllables[0])
        syllables_current += syllables[1]
        if syllables_current > 5:
            return False
        if syllables_current == 5:
            syllables_list = syllables_list[syllables_list.index(syllables) + 1:]
            break

    # Checks if there is a break at 12 total syllables to split second and third lines
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
    """Command that counts and replies with the number of syllables in the given text.

    Args:
        context: The discord.py context of the command.
        *args: The text to be counted.
    """
    sentence = " ".join(args)
    syllables = 0
    words = sentence.split()
    for word in words:
        syllables += syllapy.count(word)
    await context.reply(f'{arguments} has {syllables} syllables.')


@bot.event
async def on_message(message):
    """Event handler for new messages. Checks if the message is a haiku and sends a formatted version if it is.

    Args:
        message: The incoming message.
    """
    # Ignore messages from the bot
    if message.author == bot.user:
        return

    haiku = is_haiku(message.content)
    if haiku:
        line1 = " ".join(haiku[1][0])
        line2 = " ".join(haiku[1][1])
        line3 = " ".join(haiku[1][2])
        await message.channel.send(f"\n{line1}\n{line2}\n{line3}")

    await bot.process_commands(message)  # to allow processing commands in addition to the on_message event


bot.run(BOT_TOKEN)
