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
import config
import random
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def get_random_style():
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": random.choice(STYLES)}
    return {}

def song_markup(_, vidid):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["SG_B_2"],
                callback_data=f"song_helper audio|{vidid}",
                **get_random_style()
            ),
            InlineKeyboardButton(
                text=_["SG_B_3"],
                callback_data=f"song_helper video|{vidid}",
                **get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], 
                callback_data="close",
                **get_random_style()
            ),
        ],
    ]
    return buttons
