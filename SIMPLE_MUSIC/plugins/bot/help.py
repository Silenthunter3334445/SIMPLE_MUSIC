# -----------------------------------------------
# 🔸 SIMPLE MUSIC Project
# 🔹 Developed & Maintained by: Simple Boy (https://github.com/Simple-Boy-1k)
# 📅 Copyright © 2026 – All Rights Reserved
# -----------------------------------------------

import math
from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.utils.database import get_lang
from SIMPLE_MUSIC.utils.decorators.language import LanguageStart, languageCB
from SIMPLE_MUSIC.utils.inline.help import (
    help_pannel_page1,
    help_pannel_page2,
    help_pannel_page3,
    help_pannel_page4,
    help_back_markup,
    private_help_panel,
)
from config import BANNED_USERS, SUPPORT_CHAT, HELP_IMG_URL
from strings import get_string, helpers

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel_page1(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel_page1(_)
        await update.reply_photo(
            HELP_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(
        _["help_2"], 
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@app.on_callback_query(filters.regex(r"^help_page_") & ~BANNED_USERS)
@languageCB
async def help_page_cb(client, CallbackQuery, _):
    page = int(CallbackQuery.data.split("_")[2])
    
    if page == 1:
        keyboard = help_pannel_page1(_, True)
    elif page == 2:
        keyboard = help_pannel_page2(_, True)
    elif page == 3:
        keyboard = help_pannel_page3(_, True)
    elif page == 4:
        keyboard = help_pannel_page4(_, True)
    else:
        keyboard = help_pannel_page1(_, True)
        
    await CallbackQuery.edit_message_text(
        _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
    )


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    number = int(cb.replace("hb", ""))
    
    help_text = getattr(helpers, f"HELP_{number}", "Error: Help Text Not Found!")
    
    page_number = math.ceil(number / 9.0)
    if page_number > 4:
        page_number = 4
        
    keyboard = help_back_markup(_, page_number)
    await CallbackQuery.edit_message_text(help_text, reply_markup=keyboard)
