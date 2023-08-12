import os
import re
import textwrap
import aiofiles
import aiohttp
from PIL import (Image, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL

async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = youtube.convert("RGBA")
        background = image1.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        font_path = "assets/font2.ttf"  # Verify the correct path to font2.ttf
        font = ImageFont.truetype(font_path, 40)  # Load the font
        draw = ImageDraw.Draw(background)

        draw.text(
            (5, 5), f"{MUSIC_BOT_NAME}", fill="white", font=font
        )

        para = textwrap.wrap(title, width=32)
        for line in para:
            draw.text(
                (30, 150),
                "NOW PLAYING:",
                fill="white",
                font=font,
            )
            draw.text(
                (30, 200),
                f"{line}",
                fill="white",
                font=font,
            )

        draw.text(
            (30, 280),
            f"Duration: {duration[:23]} Mins",
            (255, 255, 255),
            font=font,
        )

        draw.text(
            (30, 350),
            "#━━━━━━━━━━━━━━━━━०━━━━━#",
            fill="white",
            font=font,
        )

        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception:
        return YOUTUBE_IMG_URL
