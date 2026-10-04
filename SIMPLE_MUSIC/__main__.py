# -----------------------------------------------
# 🔸 SIMPLE MUSIC Project
# 🔹 Developed & Maintained by: Simple Boy (https://github.com/Simple-Boy-1k)
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Simple_Boy_1k
# -----------------------------------------------

import asyncio
import importlib
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from SIMPLE_MUSIC import LOGGER, app, userbot
from SIMPLE_MUSIC.core.call import SIMPLE
from SIMPLE_MUSIC.misc import sudo
from SIMPLE_MUSIC.plugins import ALL_MODULES
from SIMPLE_MUSIC.utils.database import get_banned_users, get_gbanned

COMMANDS = [
    BotCommand("start", "❖ sᴛᴀʀᴛ ʙᴏᴛ • ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
    BotCommand("help", "❖ ʜᴇʟᴘ ᴍᴇɴᴜ • ɢᴇᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ"),
    BotCommand("ping", "❖ ᴘɪɴɢ ʙᴏᴛ • ᴄʜᴇᴄᴋ ᴘɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs"),
    BotCommand("play", "❖ ᴘʟᴀʏ ᴀᴜᴅɪᴏ ᴏɴ ᴠᴄ • ᴛᴏ ᴘʟᴀʏ ᴀɴʏ ᴀᴜᴅɪᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("vplay", "❖ ᴘʟᴀʏ ᴠɪᴅᴇᴏ ᴏɴ ᴠᴄ • ᴛᴏ sᴛʀᴇᴀᴍ ᴀɴʏ ᴠɪᴅᴇᴏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ"),
    BotCommand("playrtmps", "❖ ᴘʟᴀʏ ʟɪᴠᴇ ᴠɪᴅᴇᴏ • sᴛʀᴇᴀᴍ ʟɪᴠᴇ ᴠɪᴅᴇᴏ ᴄᴏɴᴛᴇɴᴛ"),
    BotCommand("playforce", "❖ ғᴏʀᴄᴇ ᴘʟᴀʏ ᴀᴜᴅɪᴏ • ғᴏʀᴄᴇ ᴘʟᴀʏ ᴀɴʏ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ"),
    BotCommand("vplayforce", "❖ ғᴏʀᴄᴇ ᴘʟᴀʏ ᴠɪᴅᴇᴏ • ғᴏʀᴄᴇ ᴘʟᴀʏ ᴀɴʏ ᴠɪᴅᴇᴏ ᴛʀᴀᴄᴋ"),
    BotCommand("pause", "❖ ᴘᴀᴜsᴇ sᴛʀᴇᴀᴍ • ᴘᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ"),
    BotCommand("resume", "❖ ʀᴇsᴜᴍᴇ sᴛʀᴇᴀᴍ • ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ"),
    BotCommand("skip", "❖ sᴋɪᴘ ᴛʀᴀᴄᴋ • sᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ"),
    BotCommand("end", "❖ ᴇɴᴅ sᴛʀᴇᴀᴍ • sᴛᴏᴘ ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ"),
    BotCommand("stop", "❖ sᴛᴏᴘ sᴛʀᴇᴀᴍ • sᴛᴏᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ sᴛʀᴇᴀᴍ"),
    BotCommand("queue", "❖ sʜᴏᴡ ǫᴜᴇᴜᴇ • ᴅɪsᴘʟᴀʏ ᴛʀᴀᴄᴋ ǫᴜᴇᴜᴇ ʟɪsᴛ"),
    BotCommand("auth", "❖ ᴀᴅᴅ ᴀᴜᴛʜ ᴜsᴇʀ • ᴀᴅᴅ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ʟɪsᴛ"),
    BotCommand("unauth", "❖ ʀᴇᴍᴏᴠᴇ ᴀᴜᴛʜ • ʀᴇᴍᴏᴠᴇ ᴜsᴇʀ ғʀᴏᴍ ᴀᴜᴛʜ ʟɪsᴛ"),
    BotCommand("authusers", "❖ ᴀᴜᴛʜ ʟɪsᴛ • sʜᴏᴡ ᴀʟʟ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs"),
    BotCommand("cplay", "❖ ᴄʜᴀɴɴᴇʟ ᴀᴜᴅɪᴏ • ᴘʟᴀʏ ᴀᴜᴅɪᴏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("cvplay", "❖ ᴄʜᴀɴɴᴇʟ ᴠɪᴅᴇᴏ • ᴘʟᴀʏ ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("cplayforce", "❖ ᴄʜᴀɴɴᴇʟ ғᴏʀᴄᴇ ᴀᴜᴅɪᴏ • ғᴏʀᴄᴇ ᴘʟᴀʏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("cvplayforce", "❖ ᴄʜᴀɴɴᴇʟ ғᴏʀᴄᴇ ᴠɪᴅᴇᴏ • ғᴏʀᴄᴇ ᴠɪᴅᴇᴏ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("channelplay", "❖ ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ • ʟɪɴᴋ ɢʀᴏᴜᴘ ᴛᴏ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("loop", "❖ ʟᴏᴏᴘ ᴍᴏᴅᴇ • ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ʟᴏᴏᴘ"),
    BotCommand("stats", "❖ ʙᴏᴛ sᴛᴀᴛs • sʜᴏᴡ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs"),
    BotCommand("shuffle", "❖ sʜᴜғғʟᴇ ǫᴜᴇᴜᴇ • ʀᴀɴᴅᴏᴍɪᴢᴇ ᴛʀᴀᴄᴋ ᴏʀᴅᴇʀ"),
    BotCommand("seek", "❖ sᴇᴇᴋ ғᴏʀᴡᴀʀᴅ • sᴋɪᴘ ᴛᴏ sᴘᴇᴄɪғɪᴄ ᴛɪᴍᴇ"),
    BotCommand("seekback", "❖ sᴇᴇᴋ ʙᴀᴄᴋᴡᴀʀᴅ • ɢᴏ ʙᴀᴄᴋ ᴛᴏ ᴘʀᴇᴠɪᴏᴜs ᴛɪᴍᴇ"),
    BotCommand("song", "❖ ᴅᴏᴡɴʟᴏᴀᴅ sᴏɴɢ • ɢᴇᴛ ᴍᴘ3 ᴏʀ ᴍᴘ4 ғɪʟᴇ"),
    BotCommand("speed", "❖ ᴀᴅᴊᴜsᴛ sᴘᴇᴇᴅ • ᴄʜᴀɴɢᴇ ᴘʟᴀʏʙᴀᴄᴋ sᴘᴇᴇᴅ ɪɴ ɢʀᴏᴜᴘ"),
    BotCommand("cspeed", "❖ ᴄʜᴀɴɴᴇʟ sᴘᴇᴇᴅ • ᴀᴅᴊᴜsᴛ sᴘᴇᴇᴅ ɪɴ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("tagall", "❖ ᴛᴀɢ ᴀʟʟ • ᴍᴇɴᴛɪᴏɴ ᴇᴠᴇʀʏᴏɴᴇ ɪɴ ɢʀᴏᴜᴘ"),
]


async def setup_bot_commands():
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("SIMPLE_MUSIC").info("Bot commands set successfully!")
    except Exception as e:
        LOGGER("SIMPLE_MUSIC").error(f"Failed to set bot commands: {str(e)}")


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error(
            "𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧"
        )
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)

    except:
        pass

    await app.start()
    
    await setup_bot_commands()

    for all_module in ALL_MODULES:
        importlib.import_module("SIMPLE_MUSIC.plugins" + all_module)

    LOGGER("SIMPLE_MUSIC.plugins").info(
        "𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳..."
    )

    await userbot.start()
    await SIMPLE.start()

    try:
        await SIMPLE.stream_call(
            "https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4"
        )

    except NoActiveGroupCall:
        LOGGER("SIMPLE_MUSIC").error(
            "𝗣𝗹𝗭 𝗦𝗧𝗔𝗥𝗧 𝗬𝗢𝗨𝗥 𝗟𝗢𝗚 𝗚𝗥𝗢𝗨𝗣 𝗩𝗢𝗜𝗖𝗘𝗖𝗛𝗔𝗧\\𝗖𝗛𝗔𝗡𝗡𝗘𝗟\n\n𝗦𝗜𝗠𝗣𝗟𝗘 𝗕𝗢𝗧 𝗦𝗧𝗢𝗣........"
        )
        exit()

    except:
        pass

    await SIMPLE.decorators()

    LOGGER("SIMPLE_MUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗠𝗔𝗗𝗘 𝗕𝗬 𝗦𝗜𝗠𝗣𝗟𝗘 𝗕𝗢𝗬\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await idle()

    await app.stop()
    await userbot.stop()

    LOGGER("SIMPLE_MUSIC").info(
        "𝗦𝗧𝗢𝗣 𝗦𝗜𝗠𝗣𝗟𝗘 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧.."
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())