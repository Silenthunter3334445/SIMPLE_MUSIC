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
import asyncio
import config
from SIMPLE_MUSIC import app
from pyrogram import Client, filters, enums
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

# --------------------------------------------------------------------------------- #
# Note: Image aur Font functions ko hata diya hai kyunki ab sirf text message jayega.
# --------------------------------------------------------------------------------- #

@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {
            "banned", "left", "restricted"
        }
        and member.old_chat_member
    ):
        pass
    else:
        return

    user = (
        member.old_chat_member.user
        if member.old_chat_member
        else member.from_user
    )

    try:
        # ✨ Naya aur cool text format aapke liye:
        text = (
            f"**╭─────── •🥀• ───────╮**\n"
            f"**      ɢᴏᴏᴅ ʙʏᴇ ᴍɪᴛᴛᴀʀ ᴊɪ 🥺 **\n"
            f"**╰─────── •🥀• ───────╯**\n\n"
            f"**👤 ɴᴀᴍᴇ :** {user.mention}\n"
            f"**🆔 ᴜsᴇʀ ɪᴅ :** `{user.id}`\n\n"
            f"**๏ ᴛᴀᴋᴇ ᴄᴀʀᴇ ᴅᴇᴀʀ 🥺**\n\n"
            f"**🕊️ ɢᴏᴏᴅ ʙʏᴇ & sᴛᴀʏ sᴀғᴇ...**"
        )
        
        button_text = "๏ ᴠɪᴇᴡ ᴘʀᴏғɪʟᴇ ๏"
        deep_link = f"tg://openmessage?user_id={user.id}"
        
        r1 = random.choice(STYLES)

        # Ab ye send_photo ki jagah direct send_message karega
        message = await client.send_message(
            chat_id=member.chat.id,
            text=text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(button_text, url=deep_link, **_get_style(r1))]
            ])
        )

        # 30 seconds baad message auto-delete hone ka system vaise hi rkha hai
        async def delete_message():
            await asyncio.sleep(30)
            await message.delete()

        asyncio.create_task(delete_message())
        
    except RPCError as e:
        print(e)
        return
