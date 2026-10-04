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
from typing import Union
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


def setting_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AU", **get_random_style()),
            InlineKeyboardButton(text=_["ST_B_3"], callback_data="LG", **get_random_style()),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_2"], callback_data="PM", **get_random_style()),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_4"], callback_data="VM", **get_random_style()),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", **get_random_style()),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="Vᴏᴛɪɴɢ ᴍᴏᴅᴇ ➜", callback_data="VOTEANSWER", **get_random_style()),
            InlineKeyboardButton(
                text=_["ST_B_5"] if mode == True else _["ST_B_6"],
                callback_data="VOMODECHANGE",
                **get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M", **get_random_style()),
            InlineKeyboardButton(
                text=f"ᴄᴜʀʀᴇɴᴛ : {current}",
                callback_data="ANSWERVOMODE",
                **get_random_style()
            ),
            InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A", **get_random_style()),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                **get_random_style()
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", **get_random_style()),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_7"], callback_data="AUTHANSWER", **get_random_style()),
            InlineKeyboardButton(
                text=_["ST_B_8"] if status == True else _["ST_B_9"],
                callback_data="AUTH",
                **get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AUTHLIST", **get_random_style()),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                **get_random_style()
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", **get_random_style()),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_10"], callback_data="SEARCHANSWER", **get_random_style()),
            InlineKeyboardButton(
                text=_["ST_B_11"] if Direct == True else _["ST_B_12"],
                callback_data="MODECHANGE",
                **get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_13"], callback_data="AUTHANSWER", **get_random_style()),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Group == True else _["ST_B_9"],
                callback_data="CHANNELMODECHANGE",
                **get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_14"], callback_data="PLAYTYPEANSWER", **get_random_style()),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Playtype == True else _["ST_B_9"],
                callback_data="PLAYTYPECHANGE",
                **get_random_style()
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                **get_random_style()
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", **get_random_style()),
        ],
    ]
    return buttons
