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
import requests
from bs4 import BeautifulSoup as  BSP
from SIMPLE_MUSIC import app as SIMPLE
from pyrogram import filters
url = "https://all-hashtag.com/library/contents/ajax_generator.php"

@SIMPLE.on_message(filters.command("hastag"))
async def hastag(bot, message):
    global content
    try:
        text = message.text.split(' ',1)[1]
        data = dict(keyword=text, filter="top")

        res = requests.post(url, data).text

        content = BSP(res, 'html.parser').find("div", {"class":"copy-hashtags"}).string
    except IndexError:
        return await message.reply_text("Example:\n\n/hastag python")
        
    
    await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ  ʜᴀsᴛᴀɢ :\n<pre>{content}</pre>", quote=True)
    
mod_name = "Hᴀsʜᴛᴀɢ"
help= """
Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʜᴀsʜᴛᴀɢ ɢᴇɴᴇʀᴀᴛᴏʀ ᴡʜɪᴄʜ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴛʜᴇ ᴛᴏᴘ 𝟹𝟶 ᴀɴᴅ ᴍᴏʀᴇ ʜᴀsʜᴛᴀɢs ʙᴀsᴇᴅ ᴏғғ ᴏғ ᴏɴᴇ ᴋᴇʏᴡᴏʀᴅ sᴇʟᴇᴄᴛɪᴏɴ.
° /hastag enter word to generate hastag.
°Exᴀᴍᴘʟᴇ:  /hastag python """
