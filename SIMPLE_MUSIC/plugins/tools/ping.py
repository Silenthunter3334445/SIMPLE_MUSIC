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
import random
import config
from datetime import datetime
from pyrogram import filters, enums
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import *
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.core.call import SIMPLE
from SIMPLE_MUSIC.utils import bot_sys_stats
from SIMPLE_MUSIC.utils.decorators.language import language
from SIMPLE_MUSIC.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

@app.on_message(filters.command("ping", prefixes=["/"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await SIMPLE.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    
    # Note: supp_markup is imported. You may need to add the color logic inside 
    # SIMPLE_MUSIC.utils.inline.supp_markup to apply it to the ping buttons.
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
