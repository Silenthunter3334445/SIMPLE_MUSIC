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
import requests
import config
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SIMPLE_MUSIC import app

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

def get_pypi_info(package_name):
    try:
        api_url = f"https://pypi.org/pypi/{package_name}/json"
        
        # Sending a request to the PyPI API
        response = requests.get(api_url)
        
        if response.status_code == 200:
            # Extracting information from the API response
            return response.json()
        return None
    
    except Exception as e:
        print(f"Error fetching PyPI information: {e}")
        return None

@app.on_message(filters.command("pypi", prefixes=["/", "!", "."]))
def pypi_info_command(client, message):
    try:
        package_name = message.command[1]
        
        # Getting information from PyPI
        pypi_info = get_pypi_info(package_name)
        
        if pypi_info:
            name = pypi_info['info'].get('name', 'N/A')
            version = pypi_info['info'].get('version', 'N/A')
            summary = pypi_info['info'].get('summary', 'N/A')
            project_url = pypi_info['info'].get('project_urls', {}).get('Homepage') or pypi_info['info'].get('package_url', f"https://pypi.org/project/{name}/")

            # Creating a message with PyPI information
            info_message = (
                f"📦 **ᴘᴀᴄᴋᴀɢᴇ ɴᴀᴍᴇ** ➪ `{name}`\n\n"
                f"🏷 **Lᴀᴛᴇsᴛ ᴠᴇʀsɪᴏɴ** ➪ `{version}`\n\n"
                f"📝 **Dᴇsᴄʀɪᴘᴛɪᴏɴ** ➪ {summary}"
            )
            
            r1, r2 = random.choices(STYLES, k=2)
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 ᴘʀᴏᴊᴇᴄᴛ ᴜʀʟ", url=project_url, **_get_style(r1))],
                [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close", **_get_style(r2))]
            ])
            
            # Sending the PyPI information back to the user
            client.send_message(message.chat.id, info_message, reply_markup=reply_markup)
        
        else:
            # Handling the case where information retrieval failed
            client.send_message(message.chat.id, "❌ **Failed to fetch information from PyPI.**")
    
    except IndexError:
        client.send_message(message.chat.id, "⚠️ **Please provide a package name after the /pypi command.**")
