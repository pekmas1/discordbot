import discord
from discord.ext import commands
from discord.ext.commands import Context
import os
from dotenv import load_dotenv
from pathlib import Path
import cv2

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

PARENT_DIR = Path(__file__).parent
IMAGES_DIR = PARENT_DIR / "reference_images"

def get_image_features(image_path):
    """Calculate color histogram features"""
    img = cv2.imread(str(image_path))
    # Convert to HSV color space (better for color similarity)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Calculate histogram for each HSV channel
    # Using 8 bins for Hue, 12 for Saturation, and 3 for Value
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 12, 3], [0, 180, 0, 256, 0, 256])

    # Normalize histogram
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def compare_histograms(hist1, hist2):
    """Compare two histograms using correlation"""
    # Using correlation method (other options: 'chi-square', 'bhattacharyya', 'intersect')
    return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

@bot.command()
async def search(ctx: Context):
    if not ctx.message.attachments:
        await ctx.send("Please upload an image file!")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        await ctx.send("Please upload am image file!")
        return
    
    query_path = PARENT_DIR / "query" / "query.jpg"
    await attachment.save(query_path)

    query_hist = get_image_features(query_path)

    best_match = None
    highest_similarity = -1

    for img_path in IMAGES_DIR.glob("*.jpg"):
        ref_hist = get_image_features(img_path)
        score = compare_histograms(query_hist, ref_hist)
        if score > highest_similarity:
            highest_similarity = score
            best_match = img_path
    
    if best_match:
        await ctx.send(f"Most similar image (similarity: {highest_similarity:.2f})",
                    file=discord.File(best_match))
    else:
        await ctx.send("No reference images found!")

bot.run(TOKEN)