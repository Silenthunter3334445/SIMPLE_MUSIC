# -----------------------------------------------
# 🔸 SIMPLE MUSIC Project
# 🔹 Developed & Maintained by: Simple Boy (https://github.com/Simple-Boy-1k)
# 📅 Copyright © 2026 – All Rights Reserved
# -----------------------------------------------

import config
import random
from typing import Union
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SIMPLE_MUSIC import app

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def help_pannel_page1(_, START: Union[bool, int] = None):
    s1, s2, s3 = random.sample(STYLES, 3)
    s4 = random.choice(STYLES)
    row_styles = [s1, s2, s3, s4]
    
    def get_style(index):
        if getattr(config, "BUTTON_COLOUR", False):
            return {"style": row_styles[index] if index < len(row_styles) else enums.ButtonStyle.PRIMARY}
        return {}

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3", **get_style(0)),
            ],
            [
                InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6", **get_style(1)),
            ],
            [
                InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7", **get_style(2)),
                InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8", **get_style(2)),
                InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9", **get_style(2)),
            ],
            [
                InlineKeyboardButton(text="⏮", callback_data="help_page_4", **get_style(3)),
                InlineKeyboardButton(
                    text="🏡 ʜᴏᴍᴇ" if START else _["CLOSE_BUTTON"],
                    callback_data="home" if START else "close",
                    **get_style(3)
                ),
                InlineKeyboardButton(text="⏭", callback_data="help_page_2", **get_style(3)),
            ],
        ]
    )

def help_pannel_page2(_, START: Union[bool, int] = None):
    s1, s2, s3 = random.sample(STYLES, 3)
    s4 = random.choice(STYLES)
    row_styles = [s1, s2, s3, s4]
    
    def get_style(index):
        if getattr(config, "BUTTON_COLOUR", False):
            return {"style": row_styles[index] if index < len(row_styles) else enums.ButtonStyle.PRIMARY}
        return {}

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12", **get_style(0)),
            ],
            [
                InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", **get_style(1)),
            ],
            [
                InlineKeyboardButton(text=_["H_B_16"], callback_data="help_callback hb16", **get_style(2)),
                InlineKeyboardButton(text=_["H_B_17"], callback_data="help_callback hb17", **get_style(2)),
                InlineKeyboardButton(text=_["H_B_18"], callback_data="help_callback hb18", **get_style(2)),
            ],
            [
                InlineKeyboardButton(text="⏮", callback_data="help_page_1", **get_style(3)),
                InlineKeyboardButton(
                    text="🏡 ʜᴏᴍᴇ" if START else _["CLOSE_BUTTON"],
                    callback_data="home" if START else "close",
                    **get_style(3)
                ),
                InlineKeyboardButton(text="⏭", callback_data="help_page_3", **get_style(3)),
            ],
        ]
    )

def help_pannel_page3(_, START: Union[bool, int] = None):
    s1, s2, s3 = random.sample(STYLES, 3)
    s4 = random.choice(STYLES)
    row_styles = [s1, s2, s3, s4]
    
    def get_style(index):
        if getattr(config, "BUTTON_COLOUR", False):
            return {"style": row_styles[index] if index < len(row_styles) else enums.ButtonStyle.PRIMARY}
        return {}

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_19"], callback_data="help_callback hb19", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_20"], callback_data="help_callback hb20", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_21"], callback_data="help_callback hb21", **get_style(0)),
            ],
            [
                InlineKeyboardButton(text=_["H_B_22"], callback_data="help_callback hb22", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_23"], callback_data="help_callback hb23", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_24"], callback_data="help_callback hb24", **get_style(1)),
            ],
            [
                InlineKeyboardButton(text=_["H_B_25"], callback_data="help_callback hb25", **get_style(2)),
                InlineKeyboardButton(text=_["H_B_26"], callback_data="help_callback hb26", **get_style(2)),
                InlineKeyboardButton(text=_["H_B_27"], callback_data="help_callback hb27", **get_style(2)),
            ],
            [
                InlineKeyboardButton(text="⏮", callback_data="help_page_2", **get_style(3)),
                InlineKeyboardButton(
                    text="🏡 ʜᴏᴍᴇ" if START else _["CLOSE_BUTTON"],
                    callback_data="home" if START else "close",
                    **get_style(3)
                ),
                InlineKeyboardButton(text="⏭", callback_data="help_page_4", **get_style(3)),
            ],
        ]
    )

def help_pannel_page4(_, START: Union[bool, int] = None):
    s1, s2, s3 = random.sample(STYLES, 3)
    s4 = random.choice(STYLES)
    row_styles = [s1, s2, s3, s4]
    
    def get_style(index):
        if getattr(config, "BUTTON_COLOUR", False):
            return {"style": row_styles[index] if index < len(row_styles) else enums.ButtonStyle.PRIMARY}
        return {}

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["H_B_28"], callback_data="help_callback hb28", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_29"], callback_data="help_callback hb29", **get_style(0)),
                InlineKeyboardButton(text=_["H_B_30"], callback_data="help_callback hb30", **get_style(0)),
            ],
            [
                InlineKeyboardButton(text=_["H_B_31"], callback_data="help_callback hb31", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_32"], callback_data="help_callback hb32", **get_style(1)),
                InlineKeyboardButton(text=_["H_B_33"], callback_data="help_callback hb33", **get_style(1)),
            ],
            [
                InlineKeyboardButton(text="⏮", callback_data="help_page_3", **get_style(2)),
                InlineKeyboardButton(
                    text="🏡 ʜᴏᴍᴇ" if START else _["CLOSE_BUTTON"],
                    callback_data="home" if START else "close",
                    **get_style(2)
                ),
                InlineKeyboardButton(text="⏭", callback_data="help_page_1", **get_style(2)),
            ],
        ]
    )

def help_back_markup(_, page: int = 1):
    style = {"style": random.choice(STYLES)} if getattr(config, "BUTTON_COLOUR", False) else {}
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"help_page_{page}",
                    **style
                )
            ]
        ]
    )

def private_help_panel(_):
    style = {"style": random.choice(STYLES)} if getattr(config, "BUTTON_COLOUR", False) else {}
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
                **style
            ),
        ]
    ]
