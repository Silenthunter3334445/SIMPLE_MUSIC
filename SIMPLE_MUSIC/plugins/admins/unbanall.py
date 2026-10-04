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
from SIMPLE_MUSIC import app
from config import OWNER_ID
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from SIMPLE_MUSIC.utils.Simple_ban import admin_filter

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

@app.on_message(filters.command("unbanall") & admin_filter)
async def unban_all(_, msg):
    chat_id = msg.chat.id
    x = 0
    
    # Dynamically fetch the bot's own ID using app.me.id
    bot_me = await app.get_me()
    bot = await app.get_chat_member(chat_id, bot_me.id)
    
    bot_permission = bot.privileges and bot.privileges.can_restrict_members
    if bot_permission:
        r1 = random.choice(STYLES)
        status_msg = await msg.reply_text(
            "⏳ **Unbanning all users...**", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Stop", callback_data="stop", **_get_style(r1))]])
        )
        
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            try:
                await app.unban_chat_member(chat_id, m.user.id)
                print(f"ᴜɴʙᴀɴɪɴɢ: {m.user.mention}")
                x += 1
            except Exception:
                pass
                
        try:
            await status_msg.edit_text(f"✅ **Successfully unbanned {x} users.**")
        except Exception:
            pass
    else:
        await msg.reply_text("ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.")

@app.on_callback_query(filters.regex("^stop$"))
async def stop_callback(_, query):
    await query.message.delete()
