import os
import re
import textwrap
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def gen_thumb(videoid, is_played=True, bot_username="Nobara Kugisaki!", guild_name="@JujutsuHighBotUpdates"):
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
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("assets/font2.ttf", 40)
        font2 = ImageFont.truetype("assets/font2.ttf", 70)
        arial = ImageFont.truetype("assets/font2.ttf", 30)
        name_font = ImageFont.truetype("assets/font.ttf", 30)
        para = textwrap.wrap(title, width=32)

        draw.text((30, 30), f"{bot_username} - {guild_name}", fill="white", font=name_font)
        if is_played:
            draw.text((30, 150), "YOUR QUERY", fill="white", font=font2)
        draw.text((30, 250), "NOW PLAYING", fill="white", stroke_width=2, stroke_fill="white", font=font2)

        j = 0
        for line in para:
            if j == 1:
                j += 1
                draw.text((30, 400 + (j - 1) * 60), f"{line}", fill="white", stroke_width=1, stroke_fill="white", font=font)
            if j == 0:
                j += 1
                draw.text((30, 340 + (j - 1) * 60), f"{line}", fill="white", stroke_width=1, stroke_fill="white", font=font)

        draw.text((30, 560), f"Views : {views[:23]}", (255, 255, 255), font=arial)
        draw.text((30, 610), f"Duration : {duration[:23]} Mins", (255, 255, 255), font=arial)
        draw.text((30, 660), f"Channel : {channel}", (255, 255, 255), font=arial)

        telegraph_img = Image.open("assets/Nobara.jpg")
        telegraph_img = telegraph_img.resize((350, 350))
        telegraph_mask = Image.new("L", telegraph_img.size, 0)
        telegraph_draw_mask = ImageDraw.Draw(telegraph_mask)
        telegraph_draw_mask.ellipse((0, 0, 350, 350), fill=255)

        border_width = 10
        border_color = (255, 255, 255)
        bordered_telegraph_img = Image.new("RGBA", (350 + 2 * border_width, 350 + 2 * border_width), (0, 0, 0, 0))
        bordered_telegraph_img.paste(telegraph_img, (border_width, border_width), telegraph_mask) #frag glanced here 

        image_width, image_height = background.size
        telegraph_width, telegraph_height = bordered_telegraph_img.size
        x_pos = image_width - telegraph_width - 30
        y_pos = (image_height - telegraph_height) // 2

        background.paste(bordered_telegraph_img, (x_pos, y_pos), bordered_telegraph_img)

        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception:
        return YOUTUBE_IMG_URL
