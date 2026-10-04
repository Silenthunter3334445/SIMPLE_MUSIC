import asyncio
import os
import re
from typing import Optional, Union

import aiofiles
import aiohttp
import yt_dlp
from py_yt import Playlist, VideosSearch
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message

from SIMPLE_MUSIC.utils.formatters import time_to_seconds


# -------------------------------------------------
# Configuration
# -------------------------------------------------

DOWNLOAD_DIR = "downloads"

# Optional API configuration.
# These are read safely so the bot does not crash
# if one of them is missing from config.py.
try:
    from config import (
        API_URL as CONFIG_API_URL,
        VIDEO_API_URL,
        API_KEY,
        YT_API_KEY,
        YTPROXY_URL,
    )
except ImportError:
    CONFIG_API_URL = None
    VIDEO_API_URL = None
    API_KEY = None
    YT_API_KEY = None
    YTPROXY_URL = None

API_URL = CONFIG_API_URL or "https://shrutibots.site"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

CLIENT_SESSION: Optional[aiohttp.ClientSession] = None


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def get_video_id(link: str) -> str:
    """Extract a YouTube video ID from a URL or ID."""
    link = str(link).strip()

    if "v=" in link:
        return link.split("v=", 1)[1].split("&", 1)[0]

    if "youtu.be/" in link:
        return link.split("youtu.be/", 1)[1].split("?", 1)[0].split("&", 1)[0]

    if "/shorts/" in link:
        return link.split("/shorts/", 1)[1].split("?", 1)[0].split("&", 1)[0]

    if "/live/" in link:
        return link.split("/live/", 1)[1].split("?", 1)[0].split("&", 1)[0]

    return link.split("/", 1)[-1].split("?", 1)[0]


async def get_session() -> aiohttp.ClientSession:
    """Return a shared aiohttp session."""
    global CLIENT_SESSION

    if CLIENT_SESSION is None or CLIENT_SESSION.closed:
        CLIENT_SESSION = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=0)
        )

    return CLIENT_SESSION


async def close_session():
    """Close the shared aiohttp session."""
    global CLIENT_SESSION

    if CLIENT_SESSION is not None and not CLIENT_SESSION.closed:
        await CLIENT_SESSION.close()

    CLIENT_SESSION = None


async def _download_stream(
    url: str,
    path: str,
    headers: Optional[dict] = None,
) -> Optional[str]:
    """Download a remote stream to a local file."""
    try:
        session = await get_session()

        timeout = aiohttp.ClientTimeout(
            total=None,
            sock_read=30,
        )

        async with session.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True,
        ) as response:

            if response.status != 200:
                return None

            async with aiofiles.open(path, "wb") as file:
                async for chunk in response.content.iter_chunked(
                    2 * 1024 * 1024
                ):
                    if chunk:
                        await file.write(chunk)

        if os.path.exists(path) and os.path.getsize(path) > 1024:
            return path

    except Exception:
        pass

    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass

    return None


# -------------------------------------------------
# ShrutiBots API
# -------------------------------------------------

async def engine_shrutibots(
    vid_id: str,
    is_video: bool,
    path: str,
) -> Optional[str]:
    """Download using ShrutiBots API."""
    try:
        session = await get_session()
        media_type = "video" if is_video else "audio"

        async with session.get(
            f"{API_URL}/download",
            params={
                "url": vid_id,
                "type": media_type,
            },
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:

            if response.status != 200:
                return None

            data = await response.json(content_type=None)
            token = data.get("download_token")

            if not token:
                return None

        stream_url = (
            f"{API_URL}/stream/{vid_id}"
            f"?type={media_type}&token={token}"
        )

        return await _download_stream(stream_url, path)

    except Exception:
        return None


# -------------------------------------------------
# XBit / YT Proxy API
# -------------------------------------------------

async def engine_xbit(
    vid_id: str,
    is_video: bool,
    path: str,
) -> Optional[str]:
    """Download using configured YT proxy API."""
    if not YTPROXY_URL or not YT_API_KEY:
        return None

    try:
        session = await get_session()

        headers = {
            "x-api-key": YT_API_KEY,
        }

        async with session.get(
            f"{YTPROXY_URL}/info/{vid_id}",
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:

            if response.status != 200:
                return None

            data = await response.json(content_type=None)

        if data.get("status") != "success":
            return None

        stream_url = (
            data.get("video_url")
            if is_video
            else data.get("audio_url")
        )

        if not stream_url:
            return None

        return await _download_stream(
            stream_url,
            path,
            headers=headers,
        )

    except Exception:
        return None


# -------------------------------------------------
# NexGen API
# -------------------------------------------------

async def engine_nexgen(
    vid_id: str,
    is_video: bool,
    path: str,
) -> Optional[str]:
    """Download using NexGen API."""
    if not API_KEY:
        return None

    try:
        session = await get_session()

        if is_video:
            if not VIDEO_API_URL:
                return None

            url = (
                f"{VIDEO_API_URL}/video/"
                f"{vid_id}?api={API_KEY}"
            )
        else:
            url = (
                f"{API_URL}/song/"
                f"{vid_id}?api={API_KEY}"
            )

        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:

            if response.status != 200:
                return None

            data = await response.json(content_type=None)

        if str(data.get("status", "")).lower() != "done":
            return None

        stream_url = data.get("link")

        if not stream_url:
            return None

        return await _download_stream(
            stream_url,
            path,
        )

    except Exception:
        return None


# -------------------------------------------------
# yt-dlp fallback
# -------------------------------------------------

async def _ytdlp_download(
    link: str,
    is_video: bool,
    final_path: str,
) -> Optional[str]:
    """Fallback downloader using yt-dlp."""

    loop = asyncio.get_running_loop()

    def download():
        if is_video:
            format_string = (
                "bestvideo[height<=480][fps<=30]"
                "[ext=mp4]+bestaudio[ext=m4a]/best"
            )
        else:
            format_string = "bestaudio/best"

        options = {
            "format": format_string,
            "outtmpl": final_path,
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "noplaylist": True,
        }

        if not is_video:
            options["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]

        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.download([link])

    try:
        await loop.run_in_executor(None, download)

        if (
            os.path.exists(final_path)
            and os.path.getsize(final_path) > 1024
        ):
            return final_path

    except Exception:
        pass

    return None


# -------------------------------------------------
# Main download engine
# -------------------------------------------------

async def _core_download(
    link: str,
    is_video: bool,
) -> Optional[str]:
    """Try APIs first, then yt-dlp."""

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    vid_id = get_video_id(link)

    if not vid_id or len(vid_id) < 3:
        return None

    extension = "mp4" if is_video else "mp3"

    final_path = os.path.join(
        DOWNLOAD_DIR,
        f"{vid_id}.{extension}",
    )

    if (
        os.path.exists(final_path)
        and os.path.getsize(final_path) > 1024
    ):
        return final_path

    temp_paths = [
        f"{final_path}.shruti",
        f"{final_path}.xbit",
        f"{final_path}.nexgen",
    ]

    tasks = [
        asyncio.create_task(
            engine_shrutibots(
                vid_id,
                is_video,
                temp_paths[0],
            )
        ),
        asyncio.create_task(
            engine_xbit(
                vid_id,
                is_video,
                temp_paths[1],
            )
        ),
        asyncio.create_task(
            engine_nexgen(
                vid_id,
                is_video,
                temp_paths[2],
            )
        ),
    ]

    winner = None

    try:
        for future in asyncio.as_completed(tasks):
            try:
                result = await future

                if result and os.path.exists(result):
                    winner = result
                    break

            except Exception:
                continue

    finally:
        for task in tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

    if winner and os.path.exists(winner):
        try:
            if os.path.exists(final_path):
                os.remove(final_path)

            os.replace(winner, final_path)
            return final_path

        except Exception:
            return winner

    # API failed -> yt-dlp fallback
    return await _ytdlp_download(
        link,
        is_video,
        final_path,
    )


# -------------------------------------------------
# Public download functions
# -------------------------------------------------

async def download_song(link: str) -> Optional[str]:
    """Download YouTube audio."""
    return await _core_download(
        link,
        is_video=False,
    )


async def download_video(link: str) -> Optional[str]:
    """Download YouTube video."""
    return await _core_download(
        link,
        is_video=True,
    )


# -------------------------------------------------
# YouTube API class
# -------------------------------------------------

class YouTubeAPI:

    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="

        self.reg = re.compile(
            r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])"
        )

    # -------------------------------------------------
    # Check YouTube URL
    # -------------------------------------------------

    async def exists(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + str(link)

        return bool(
            re.search(
                self.regex,
                str(link),
                re.IGNORECASE,
            )
        )

    # -------------------------------------------------
    # Extract URL from Telegram message
    # -------------------------------------------------

    async def url(
        self,
        message_1: Message,
    ) -> Optional[str]:

        messages = [message_1]

        if message_1.reply_to_message:
            messages.append(
                message_1.reply_to_message
            )

        for message in messages:

            # Normal URL entities
            for entity in (message.entities or []):
                if entity.type == MessageEntityType.URL:
                    text = message.text or message.caption

                    if text:
                        return text[
                            entity.offset:
                            entity.offset + entity.length
                        ]

            # Text-link entities
            for entity in (message.caption_entities or []):
                if entity.type == MessageEntityType.TEXT_LINK:
                    return entity.url

        return None

    # -------------------------------------------------
    # Video details
    # -------------------------------------------------

    async def details(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + str(link)

        if "&" in link:
            link = link.split("&")[0]

        try:
            results = VideosSearch(
                link,
                limit=1,
            )

            data = await results.next()
            items = data.get("result") or []

            if not items:
                return None

            result = items[0]

            title = result.get("title")
            duration_min = result.get("duration")
            thumbnail_list = result.get("thumbnails") or []

            thumbnail = (
                thumbnail_list[0].get("url", "").split("?")[0]
                if thumbnail_list
                else None
            )

            vidid = result.get("id")

            try:
                duration_sec = (
                    int(time_to_seconds(duration_min))
                    if duration_min
                    else 0
                )
            except Exception:
                duration_sec = 0

            return (
                title,
                duration_min,
                duration_sec,
                thumbnail,
                vidid,
            )

        except Exception:
            return None

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    async def title(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        details = await self.details(
            link,
            videoid,
        )

        return details[0] if details else None

    # -------------------------------------------------
    # Duration
    # -------------------------------------------------

    async def duration(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        details = await self.details(
            link,
            videoid,
        )

        return details[1] if details else None

    # -------------------------------------------------
    # Thumbnail
    # -------------------------------------------------

    async def thumbnail(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        details = await self.details(
            link,
            videoid,
        )

        return details[3] if details else None

    # -------------------------------------------------
    # Video
    # -------------------------------------------------

    async def video(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + str(link)

        if "&" in link:
            link = link.split("&")[0]

        try:
            downloaded_file = await download_video(
                link
            )

            if downloaded_file:
                return 1, downloaded_file

            return 0, "Video download failed"

        except Exception as e:
            return 0, f"Video download error: {e}"

    # -------------------------------------------------
    # Playlist
    # -------------------------------------------------

    async def playlist(
        self,
        link,
        limit,
        user_id,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.listbase + str(link)

        if "&" in link:
            link = link.split("&")[0]

        try:
            playlist = await Playlist.get(link)
        except Exception:
            return []

        videos = playlist.get("videos") or []

        ids = []

        for data in videos[:limit]:

            if not data:
                continue

            vid = data.get("id")

            if not vid:
                continue

            ids.append(vid)

        return ids

    # -------------------------------------------------
    # Track information
    # -------------------------------------------------

    async def track(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + str(link)

        if "&" in link:
            link = link.split("&")[0]

        try:
            results = VideosSearch(
                link,
                limit=1,
            )

            data = await results.next()
            items = data.get("result") or []

            if not items:
                return None, None

            result = items[0]

            thumbnail_list = result.get("thumbnails") or []

            thumbnail = (
                thumbnail_list[0].get("url", "").split("?")[0]
                if thumbnail_list
                else None
            )

            track_details = {
                "title": result.get("title"),
                "link": result.get("link"),
                "vidid": result.get("id"),
                "duration_min": result.get("duration"),
                "thumb": thumbnail,
            }

            return (
                track_details,
                result.get("id"),
            )

        except Exception:
            return None, None

    # -------------------------------------------------
    # Available formats
    # -------------------------------------------------

    async def formats(
        self,
        link: str,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + str(link)

        if "&" in link:
            link = link.split("&")[0]

        formats_available = []

        try:
            options = {
                "quiet": True,
                "no_warnings": True,
                "nocheckcertificate": True,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(
                    link,
                    download=False,
                )

                if not info:
                    return [], link

                for fmt in info.get("formats", []):

                    try:
                        format_name = str(
                            fmt.get("format", "")
                        )

                        if "dash" in format_name.lower():
                            continue

                        formats_available.append(
                            {
                                "format": fmt.get("format"),
                                "filesize": fmt.get("filesize"),
                                "format_id": fmt.get("format_id"),
                                "ext": fmt.get("ext"),
                                "format_note": fmt.get(
                                    "format_note"
                                ),
                                "yturl": link,
                            }
                        )

                    except Exception:
                        continue

        except Exception:
            return [], link

        return formats_available, link

    # -------------------------------------------------
    # Slider / Search results
    # -------------------------------------------------

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + str(link)

        if "&" in link:
            link = link.split("&")[0]

        try:
            search = VideosSearch(
                link,
                limit=10,
            )

            data = await search.next()
            results = data.get("result") or []

            if (
                query_type < 0
                or query_type >= len(results)
            ):
                return None

            result = results[query_type]

            thumbnail_list = (
                result.get("thumbnails") or []
            )

            thumbnail = (
                thumbnail_list[0].get("url", "").split("?")[0]
                if thumbnail_list
                else None
            )

            return (
                result.get("title"),
                result.get("duration"),
                thumbnail,
                result.get("id"),
            )

        except Exception:
            return None

    # -------------------------------------------------
    # Main download method
    # -------------------------------------------------

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ):

        if videoid:
            link = self.base + str(link)

        if "&" in link:
            link = link.split("&")[0]

        try:
            is_video = bool(video)

            if is_video:
                downloaded_file = await download_video(
                    link
                )
            else:
                downloaded_file = await download_song(
                    link
                )

            if downloaded_file:
                return downloaded_file, True

            return None, False

        except Exception:
            return None, False


# -------------------------------------------------
# Global instance
# -------------------------------------------------

YouTube = YouTubeAPI()
