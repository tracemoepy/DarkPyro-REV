# Part of PyroMan - 2022
# Kang by DarkPyro - 2023

import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import BOTLOG_CHATID
from ProjectDark.helpers.SQL.globals import CMD_HANDLER as cmd
from ProjectDark.helpers.basic import edit_or_reply
from ProjectDark.utils.misc import extract_args

from .help import add_command_help

commands = ["spam", "statspam", "slowspam", "fastspam"]
SPAM_COUNT = [0]


def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 50


@Client.on_message(filters.me & filters.command("dspam", cmd))
async def delayspam(client: Client, message: Message):
    delayspam = await extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        await message.edit("Something went wrong!")
        return
    delay = int(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], "", 1)
    spam_message = spam_message.replace(arr[1], "", 1).strip()
    await message.delete()

    if not spam_allowed():
        return

    for i in range(0, count):
        if i != 0:
            await asyncio.sleep(delay)
        await client.send_message(message.chat.id, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    await client.send_message(
        BOTLOG_CHATID, "#DELAYSPAM\nDelay spam was executed successfully!"
    )


@Client.on_message(filters.command(commands, cmd) & filters.me)
async def sspam(client: Client, message: Message):
    amount = int(message.command[1])
    text = " ".join(message.command[2:])

    cooldown = {"spam": 0.5, "statspam": 0.5, "slowspam": 1, "fastspam": 0.25}

    await message.delete()

    for msg in range(amount):
        if message.reply_to_message:
            sent = await message.reply_to_message.reply(text)
        else:
            sent = await client.send_message(message.chat.id, text)

        if message.command[0] == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()

        await asyncio.sleep(cooldown[message.command[0]])


@Client.on_message(
    filters.me & filters.command("sspam", cmd)
)
async def spam_stick(client: Client, message: Message):
    if not message.reply_to_message:
        await edit_or_reply(
            message, "Reply to a sticker with amount you want to spam!"
        )
        return
    if not message.reply_to_message.sticker:
        await edit_or_reply(
            message, "Reply to a sticker with amount you want to spam!"
        )
        return
    else:
        i = 0
        times = message.command[1]
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)

        if message.chat.type == enums.ChatType.PRIVATE:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(message.chat.id, sticker)
                await asyncio.sleep(0.10)


add_command_help(
    "spam",
    [
        ["spam <amounts> <text>",
        "Spam text."
        ],
        
        ["dspam <seconds> <amounts> <text>",
        "For delay spam",
        ],
        
        ["sspam <reply to sticker> <amounts>",
        "Spam sticker."
        ],
    ],
)
