import os
import aiofiles
import aiohttp
from PIL import Image, ImageFont, ImageDraw, ImageOps
from youtubesearchpython.__future__ import VideosSearch
import textwrap  # Import the textwrap module

async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        # Load bot logo image and font
        bot_logo = Image.open("assets/Nobara.jpg").convert("RGBA")  # Convert to RGBA mode
        bot_logo = ImageOps.fit(bot_logo, (100, 100), method=0, bleed=0.0, centering=(0.5, 0.5))  # Resize and crop to a circular shape
        mask = Image.new("L", bot_logo.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bot_logo.size, fill=255)
        bot_logo.putalpha(mask)
        
        bot_font = ImageFont.truetype("assets/font.ttf", 20)  # Specify the correct font file

        # Open and process thumbnail image
        thumbnail_image = Image.open(f"cache/thumb{videoid}.png")
        thumbnail_image.paste(bot_logo, (10, 10), bot_logo)

        bot_name = "Nobara Kugisaki!"  # Replace with your bot's name
        
        # Create a drawing context for the thumbnail image
        draw = ImageDraw.Draw(thumbnail_image)
        
        # Wrap the bot's name using textwrap
        wrapped_name = "\n".join(textwrap.wrap(bot_name, width=10))  # Adjust the width as needed
        
        # Calculate text size using ImageDraw's textsize method
        text_width, text_height = draw.textsize(wrapped_name, font=bot_font)
        
        draw.text(((thumbnail_image.width - text_width) // 2, 10 + bot_logo.height + 10),
                  wrapped_name, fill="white", font=bot_font)

        thumbnail_image.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception as e:
        print(f"An exception occurred: {e}")
     #   return "https://example.com/default_thumbnail.jpg"  # Replace with your default/fallback image URL

        return YOUTUBE_IMG_URL
##
