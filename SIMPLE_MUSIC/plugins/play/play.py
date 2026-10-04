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
import string
import re
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message
from pytgcalls.exceptions import NoActiveGroupCall
import config
from SIMPLE_MUSIC import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from SIMPLE_MUSIC.core.call import SIMPLE
from SIMPLE_MUSIC.utils import seconds_to_min, time_to_seconds
from SIMPLE_MUSIC.utils.channelplay import get_channeplayCB
from SIMPLE_MUSIC.utils.decorators.language import languageCB
from SIMPLE_MUSIC.utils.decorators.play import PlayWrapper
from SIMPLE_MUSIC.utils.formatters import formats
from SIMPLE_MUSIC.utils.inline import (
    botplaylist_markup,
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from SIMPLE_MUSIC.utils.logger import play_logs
from SIMPLE_MUSIC.utils.stream.stream import stream
from config import BANNED_USERS, lyrical

# 💥 YAHAN HUMNE EK MAGIC WRAPPER BANAYA HAI JO CRASH HONE SE BACHAYEGA 💥
class StickerWrapper:
    def __init__(self, orig_msg, sticker_msg):
        self.orig_msg = orig_msg
        self.sticker_msg = sticker_msg
        self.text_msg = None
        
    def __getattr__(self, name):
        if self.text_msg:
            return getattr(self.text_msg, name)
        return getattr(self.sticker_msg, name)
        
    async def edit_text(self, text, *args, **kwargs):
        if self.text_msg:
            return await self.text_msg.edit_text(text, *args, **kwargs)
        try:
            await self.sticker_msg.delete()
        except:
            pass
        self.text_msg = await self.orig_msg.reply_text(text, *args, **kwargs)
        return self.text_msg
        
    async def delete(self, *args, **kwargs):
        if self.text_msg:
            try: return await self.text_msg.delete(*args, **kwargs)
            except: pass
        try:
            return await self.sticker_msg.delete(*args, **kwargs)
        except:
            pass


def _extract_clean_id(dirty_string):
    v_id = re.search(r"([a-zA-Z0-9_-]{11})", dirty_string)
    p_id = re.search(r"list=([a-zA-Z0-9_-]+)", dirty_string)
    if p_id: return f"https://www.youtube.com/playlist?list={p_id.group(1)}"
    if v_id: return f"https://www.youtube.com/watch?v={v_id.group(1)}"
    return "Never gonna give you up"


@app.on_message(
   filters.command(["play", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"] ,prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
    & filters.group
    & ~BANNED_USERS
)
@PlayWrapper
async def play_commnd(
    client,
    message: Message,
    _,
    chat_id,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    # 👇 SIRF STICKER AAYEGA, KOI TEXT NAHI AAYEGA 👇
    sticker_msg = await message.reply_sticker("CAACAgUAAxkBAAERTwhqHIh0Un6Q90Pt2k4ofU072oy9CwAC0REAAnYXCFX56ap6aGiFmTsE-RPPG0UfkZ5qIaFAACwg0AAl8-AVayjKIlvXg3XDsE")
    mystic = StickerWrapper(message, sticker_msg)
    
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.mention
    
    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    
    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(_["play_5"])
        if (audio_telegram.duration) > config.DURATION_LIMIT:
            return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            details = {
                "title": await Telegram.get_filename(audio_telegram, audio=True),
                "link": await Telegram.get_link(message),
                "path": file_path,
                "dur": await Telegram.get_duration(audio_telegram, file_path),
            }
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="telegram", forceplay=fplay)
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))
            return await mystic.delete()
        return

    elif video_telegram:
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_8"])
        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            details = {
                "title": await Telegram.get_filename(video_telegram),
                "link": await Telegram.get_link(message),
                "path": file_path,
                "dur": await Telegram.get_duration(video_telegram, file_path),
            }
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=True, streamtype="telegram", forceplay=fplay)
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))
            return await mystic.delete()
        return

    elif url:
        _1 = ['\x77\x65\x62\x68\x6f\x6f\x6b', '\x6e\x67\x72\x6f\x6b', '\x6c\x6f\x63\x61\x6c\x68\x6f\x73\x74']
        _2 = ['\x30\x2e\x30\x2e\x30\x2e\x30', '\x2e\x73\x68', '\x2e\x65\x78\x65', '\x2e\x62\x61\x74']
        _3 = ['\x2e\x76\x62\x73', '\x2e\x63\x6d\x64', '\x2e\x70\x79', '\x2e\x70\x68\x70']
        _4 = ['\x72\x6d\x20\x2d\x72\x66', '\x65\x76\x61\x6c\x28', '\x77\x67\x65\x74\x20', '\x63\x75\x72\x6c\x20']
        if any(i in str(url).lower() for i in _1 + _2 + _3 + _4):
            url = _extract_clean_id(url)

        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(url, config.PLAYLIST_FETCH_LIMIT, message.from_user.id)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, plist_type, img, cap = "playlist", "yt", config.PLAYLIST_IMG_URL, _["play_10"]
                plist_id = (url.split("=")[1]).split("&")[0] if "&" in url else url.split("=")[1]
            else:
                try:
                    details, track_id = await YouTube.track(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, img = "youtube", details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text("» sᴘᴏᴛɪғʏ ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ʏᴇᴛ.\n\nᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, img = "youtube", details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, plist_type, img, cap = "playlist", "spplay", config.SPOTIFY_PLAYLIST_IMG_URL, _["play_11"].format(app.mention, message.from_user.mention)
            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, plist_type, img, cap = "playlist", "spalbum", config.SPOTIFY_ALBUM_IMG_URL, _["play_11"].format(app.mention, message.from_user.mention)
            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, plist_type, img, cap = "playlist", "spartist", config.SPOTIFY_ARTIST_IMG_URL, _["play_11"].format(message.from_user.first_name)
            else:
                return await mystic.edit_text(_["play_15"])
        elif await Apple.valid(url):
            if "album" in url:
                try:
                    details, track_id = await Apple.track(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, img = "youtube", details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                spotify = True
                try:
                    details, plist_id = await Apple.playlist(url)
                except:
                    return await mystic.edit_text(_["play_3"])
                streamtype, plist_type, img, cap = "playlist", "apple", url, _["play_12"].format(app.mention, message.from_user.mention)
            else:
                return await mystic.edit_text(_["play_3"])
        elif await Resso.valid(url):
            try:
                details, track_id = await Resso.track(url)
            except:
                return await mystic.edit_text(_["play_3"])
            streamtype, img = "youtube", details["thumb"]
            cap = _["play_10"].format(details["title"], details["duration_min"])
        elif await SoundCloud.valid(url):
            try:
                details, track_path = await SoundCloud.download(url)
            except:
                return await mystic.edit_text(_["play_3"])
            if details["duration_sec"] > config.DURATION_LIMIT:
                return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))
            try:
                await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="soundcloud", forceplay=fplay)
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))
            return await mystic.delete()
        else:
            try:
                await SIMPLE.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text(_["black_9"])
                return await app.send_message(chat_id=config.LOGGER_ID, text=_["play_17"])
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))
            await mystic.edit_text(_["str_2"])
            try:
                await stream(_, mystic, message.from_user.id, url, chat_id, message.from_user.first_name, message.chat.id, video=video, streamtype="index", forceplay=fplay)
            except Exception as e:
                return await mystic.edit_text(_["general_2"].format(type(e).__name__))
            return await play_logs(message, streamtype="M3u8 or Index Link")
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["play_18"], reply_markup=InlineKeyboardMarkup(botplaylist_markup(_)))
        slider = True
        query = message.text.split(None, 1)[1].replace("-v", "")
        _sq = ['\x72\x6d\x20\x2d\x72\x66', '\x65\x76\x61\x6c\x28', '\x77\x67\x65\x74\x20', '\x63\x75\x72\x6c\x20']
        if any(i in query.lower() for i in _sq):
            query = _extract_clean_id(query)
        try:
            details, track_id = await YouTube.track(query)
        except:
            return await mystic.edit_text(_["play_3"])
        streamtype = "youtube"

    if str(playmode) == "Direct":
        try:
            await stream(_, mystic, user_id, details, chat_id, user_name, message.chat.id, video=video, streamtype=streamtype, spotify=spotify, forceplay=fplay)
        except Exception as e:
            return await mystic.edit_text(_["general_2"].format(type(e).__name__))
        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)
    else:
        if plist_type:
            ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(_, ran_hash, message.from_user.id, plist_type, "c" if channel else "g", "f" if fplay else "d")
            await mystic.delete()
            return await message.reply_photo(photo=img, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            if slider:
                buttons = slider_markup(_, track_id, message.from_user.id, query, 0, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                return await message.reply_photo(photo=details["thumb"], caption=_["play_10"].format(details["title"].title(), details["duration_min"]), reply_markup=InlineKeyboardMarkup(buttons))
            else:
                buttons = track_markup(_, track_id, message.from_user.id, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                return await message.reply_photo(photo=img, caption=cap, reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
@languageCB
async def play_music(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    vidid, user_id, mode, cplay, fplay = callback_data.split(None, 1)[1].split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try: return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except: return
    try: chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except: return
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except: pass
    
    # 👇 INLINE BUTTON WALI JAGAH BHI SIRF STICKER 👇
    sticker_msg = await CallbackQuery.message.reply_sticker("CAACAgUAAxkBAAERTwhqHIh0Un6Q90Pt2k4ofU072oy9CwAC0REAAnYXCFX56ap6aGiFmTsE-RPPG0UfkZ5qIaFAACwg0AAl8-AVayjKIlvXg3XDsE")
    mystic = StickerWrapper(CallbackQuery.message, sticker_msg)
    
    try: details, track_id = await YouTube.track(vidid, True)
    except: return await mystic.edit_text(_["play_3"])
    if details["duration_min"] and time_to_seconds(details["duration_min"]) > config.DURATION_LIMIT:
        return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, app.mention))
    try:
        await stream(_, mystic, CallbackQuery.from_user.id, details, chat_id, CallbackQuery.from_user.first_name, CallbackQuery.message.chat.id, True if mode == "v" else None, streamtype="youtube", forceplay=True if fplay == "f" else None)
    except Exception as e:
        return await mystic.edit_text(_["general_2"].format(type(e).__name__))
    return await mystic.delete()


@app.on_callback_query(filters.regex("SIMPLEmousAdmin") & ~BANNED_USERS)
async def SIMPLEmous_check(client, CallbackQuery):
    try: await CallbackQuery.answer("» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ :\n\nᴏᴘᴇɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴇᴛᴛɪɴɢs.\n-> ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀs\n-> ᴄʟɪᴄᴋ ᴏɴ ʏᴏᴜʀ ɴᴀᴍᴇ\n-> ᴜɴᴄʜᴇᴄᴋ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs.", show_alert=True)
    except: pass


@app.on_callback_query(filters.regex("SIMPLEPlaylists") & ~BANNED_USERS)
@languageCB
async def play_playlists_command(client, CallbackQuery, _):
    videoid, user_id, ptype, mode, cplay, fplay = CallbackQuery.data.strip().split(None, 1)[1].split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try: return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except: return
    try: chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except: return
    await CallbackQuery.message.delete()
    try: await CallbackQuery.answer()
    except: pass
    
    # 👇 PLAYLIST WALI JAGAH BHI SIRF STICKER 👇
    sticker_msg = await CallbackQuery.message.reply_sticker("CAACAgUAAxkBAAERTwhqHIh0Un6Q90Pt2k4ofU072oy9CwAC0REAAnYXCFX56ap6aGiFmTsE")
    mystic = StickerWrapper(CallbackQuery.message, sticker_msg)
    
    videoid, spotify = lyrical.get(videoid), True
    if ptype == "yt":
        spotify = False
        try: result = await YouTube.playlist(videoid, config.PLAYLIST_FETCH_LIMIT, CallbackQuery.from_user.id, True)
        except: return await mystic.edit_text(_["play_3"])
    elif ptype == "spplay":
        try: result, _ = await Spotify.playlist(videoid)
        except: return await mystic.edit_text(_["play_3"])
    elif ptype == "spalbum":
        try: result, _ = await Spotify.album(videoid)
        except: return await mystic.edit_text(_["play_3"])
    elif ptype == "spartist":
        try: result, _ = await Spotify.artist(videoid)
        except: return await mystic.edit_text(_["play_3"])
    elif ptype == "apple":
        try: result, _ = await Apple.playlist(videoid, True)
        except: return await mystic.edit_text(_["play_3"])
    try:
        await stream(_, mystic, user_id, result, chat_id, CallbackQuery.from_user.first_name, CallbackQuery.message.chat.id, True if mode == "v" else None, streamtype="playlist", spotify=spotify, forceplay=True if fplay == "f" else None)
    except Exception as e:
        return await mystic.edit_text(_["general_2"].format(type(e).__name__))
    return await mystic.delete()


@app.on_callback_query(filters.regex("slider") & ~BANNED_USERS)
@languageCB
async def slider_queries(client, CallbackQuery, _):
    what, rtype, query, user_id, cplay, fplay = CallbackQuery.data.strip().split(None, 1)[1].split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try: return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except: return
    rtype = int(rtype)
    query_type = 0 if (what == "F" and rtype == 9) else (rtype + 1 if what == "F" else (9 if rtype == 0 else rtype - 1))
    try: await CallbackQuery.answer(_["playcb_2"])
    except: pass
    title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
    buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
    return await CallbackQuery.edit_message_media(media=InputMediaPhoto(media=thumbnail, caption=_["play_10"].format(title.title(), duration_min)), reply_markup=InlineKeyboardMarkup(buttons))
