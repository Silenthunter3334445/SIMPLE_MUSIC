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
from traceback import format_exc
from pyrogram import enums, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.stackoverflow import Search as StackSearch
from search_engine_parser.core.exceptions import NoResultsFound, NoResultsOrTrafficError
from SIMPLE_MUSIC import app
import config

gsearch = GoogleSearch()
stsearch = StackSearch()

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

def btn(text, value, type="callback_data", **kwargs):
    return InlineKeyboardButton(text, **{type: value}, **kwargs)

def ikb(rows=None, back=False, todo="start_back"):
    """
    rows = pass the rows
    back - if want to make back button
    todo - callback data of back button
    """
    if rows is None:
        rows = []
    lines = []
    try:
        for row in rows:
            line = []
            row_style = _get_style(random.choice(STYLES))
            for button in row:
                btn_text = button.split(".")[1].capitalize()
                button = btn(btn_text, button, **row_style)  
                line.append(button)
            lines.append(line)
    except AttributeError:
        for row in rows:
            line = []
            row_style = _get_style(random.choice(STYLES))
            for button in row:
                button = btn(*button, **row_style)  
                line.append(button)
            lines.append(line)
    except TypeError:
        # make a code to handel that error
        line = []
        row_style = _get_style(random.choice(STYLES))
        for button in rows:
            button = btn(*button, **row_style)  
            line.append(button)
        lines.append(line)
    if back: 
        row_style = _get_style(random.choice(STYLES))
        back_btn = [(btn("ʙᴀᴄᴋ", todo, **row_style))]
        lines.append(back_btn)
    return InlineKeyboardMarkup(inline_keyboard=lines)


@app.on_message(filters.command('google'))
async def search_(app: app, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**ɢɪᴠᴇ ǫᴜᴇʀʏ ᴛᴏ sᴇᴀʀᴄʜ**")
    to_del = await msg.reply_text("**sᴇᴀʀᴄʜɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ...**")
    query = split[1]
    try:
        result = await gsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"**ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ʀᴇsᴜʟᴛs ᴏғ ʀǫᴜᴇsᴛᴇᴅ : {query.title()}**"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("**ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴄᴏʀʀᴇsᴘᴏɴᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ǫᴜᴇʀʏ**")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("****ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴅᴜᴇ ᴛᴏ ᴛᴏᴏ ᴍᴀɴʏ ᴛʀᴀғғɪᴄ**")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"**sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ :\nʀᴇᴘᴏʀᴛ ᴀᴛ ɪᴛ** @Simple_Boy_1k")
        print(f"error : {e}")
        return


@app.on_message(filters.command('stack'))
async def stack_search_(app: app, msg: Message):
    split = msg.text.split(None, 1)
    if len(split) == 1:
        return await msg.reply_text("**ɢɪᴠᴇ ǫᴜᴇʀʏ ᴛᴏ sᴇᴀʀᴄʜ**")
    to_del = await msg.reply_text("**sᴇᴀʀᴄʜɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ...**")
    query = split[1]
    try:
        result = await stsearch.async_search(query)
        keyboard = ikb(
            [
                [
                    (
                        f"{result[0]['titles']}",
                        f"{result[0]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[1]['titles']}",
                        f"{result[1]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[2]['titles']}",
                        f"{result[2]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[3]['titles']}",
                        f"{result[3]['links']}",
                        "url",
                    ),
                ],
                [
                    (
                        f"{result[4]['titles']}",
                        f"{result[4]['links']}",
                        "url",
                    ),
                ],
            ]
        )

        txt = f"**ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ʀᴇsᴜʟᴛs ᴏғ ʀǫᴜᴇsᴛᴇᴅ : {query.title()}**"
        await to_del.delete()
        await msg.reply_text(txt, reply_markup=keyboard)
        return
    except NoResultsFound:
        await to_del.delete()
        await msg.reply_text("**ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴄᴏʀʀᴇsᴘᴏɴᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ǫᴜᴇʀʏ**")
        return
    except NoResultsOrTrafficError:
        await to_del.delete()
        await msg.reply_text("****ɴᴏ ʀᴇsᴜʟᴛ ғᴏᴜɴᴅ ᴅᴜᴇ ᴛᴏ ᴛᴏᴏ ᴍᴀɴʏ ᴛʀᴀғғɪᴄ**")
        return
    except Exception as e:
        await to_del.delete()
        await msg.reply_text(f"**sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ :\nʀᴇᴘᴏʀᴛ ᴀᴛ ɪᴛ** @Simple_Boy_1k")
        print(f"error : {e}")
        return
