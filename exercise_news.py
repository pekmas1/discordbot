import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import tempfile
import glob
import re
from gtts import gTTS

# โหลดตัวแปรสภาพแวดล้อม
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# ตั้งค่า bot ด้วย intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# เก็บข้อมูลข่าว
news_files = []
news_titles = []

# ID ของห้องเสียงที่จะส่งข่าว
VOICE_CHANNEL_ID = 1276744854105362453

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
    # โหลดไฟล์ข่าวและชื่อข่าว
    load_news_files()
    
    # ส่งรายการข่าวไปยังห้องเสียงที่กำหนด
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        await send_news_to_voice_channel(voice_channel)


def load_news_files():
    """โหลดไฟล์ข่าวและดึงชื่อข่าว"""
    global news_files, news_titles
    news_files = glob.glob("news/*.txt")
    news_titles = []
    
    for file_path in news_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            news_titles.append(first_line)

async def send_news_to_voice_channel(voice_channel):
    """ส่งรายการข่าวไปยังห้องเสียง"""
    # ตรวจสอบว่ามีไฟล์ข่าวหรือไม่ และจัดการกรณีที่ไม่มีข่าว
    if len(news_files) == 0:
        # ส่งข้อความไปยังห้องเสียงว่าไม่พบข่าว
        # คำแนะนำ: ใช้ voice_channel.send() เพื่อส่งข้อความไปยังห้องเสียง
        await voice_channel.send("ไม่เจอข่าวเลย ข่าวอยู่ไสส")
        return
    
    # สร้างข้อความสำหรับแสดงรายการข่าวที่มี
    # คำแนะนำ: สร้างข้อความเริ่มต้นด้วยหัวข้อสำหรับรายการข่าว
    text = "ข่าวสดๆร้อนๆ"+"\n\n"
    
    # เพิ่มชื่อข่าวแต่ละรายการพร้อมหมายเลข
    # คำแนะนำ: ใช้ enumerate() เพื่อรับทั้งดัชนีและชื่อข่าว โดยเริ่มนับจาก 1
    for i ,title in enumerate(news_titles):
        # คำแนะนำ: ใช้การจัดรูปแบบสตริงเพื่อเพิ่มหมายเลขและชื่อข่าวลงในข้อความ
        text = text + str(i+1) + " " + title + "\n"

    # เพิ่มคำแนะนำวิธีการใช้คำสั่ง read_news
    # คำแนะนำ: เพิ่มบรรทัดใหม่และคำแนะนำสำหรับการใช้คำสั่ง
    text += "ใช้ !read_news ตามด้วยตัวเลขเพื่อเลือกข่าวที่จะอ่าน"
    
    # ส่งข้อความไปยังห้องเสียง
    # คำแนะนำ: ใช้ voice_channel.send() เพื่อส่งข้อความ
    await voice_channel.send(text)

@bot.command(name='read_news')
async def read_news(ctx, number: int):
    """อ่านข่าวในห้องเสียง"""
    
    # ตรวจสอบว่าหมายเลขที่ผู้ใช้ป้อนถูกต้องหรือไม่
    # คำแนะนำ: ตรวจสอบว่า number อยู่ระหว่าง 1 ถึงความยาวของ news_files
    if (number <= 0) or (number > len(news_files)): 
        # ส่งข้อความแจ้งช่วงหมายเลขที่ถูกต้อง
        # คำแนะนำ: ใช้ ctx.send() เพื่อส่งข้อความแจ้งช่วงที่ถูกต้อง
        await ctx.send("ไปใส่เลขใหม่")
        return
    
    # ดึงข้อมูลไฟล์ข่าวและชื่อข่าวที่เลือก
    # คำแนะนำ: อาร์เรย์เริ่มจาก 0 แต่หมายเลขที่แสดงเริ่มจาก 1
    file_path = news_files[number-1]
    title = news_titles[number-1]
    
    try:
        # อ่านเนื้อหาของไฟล์ข่าว
        # คำแนะนำ: เปิดไฟล์ด้วยการเข้ารหัสที่ถูกต้อง
        with open(file_path,"r",encoding="utf-8") as file:
            # คำแนะนำ: อ่านเนื้อหาทั้งหมดของไฟล์
            content = file.read()
        
        # สร้างไฟล์ชั่วคราวสำหรับเสียง
        temp_filename = None
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_filename = temp_file.name
        
        # แจ้งผู้ใช้ว่ากำลังสร้างไฟล์เสียง
        # คำแนะนำ: ใช้ ctx.send() เพื่อแจ้งผู้ใช้ว่ากำลังสร้างเสียง
        await ctx.send("สร้างเสียงงงง")
        
        # สร้างไฟล์เสียงด้วย gTTS
        # คำแนะนำ: สร้างออบเจ็กต์ gTTS ด้วยเนื้อหาและภาษา
        tts = gTTS(content,lang="en",slow=False)
        # คำแนะนำ: บันทึกเสียงลงในไฟล์ชั่วคราว
        tts.save(temp_filename)
        
        # เชื่อมต่อกับห้องเสียง
        # คำแนะนำ: ดึงห้องเสียงโดยใช้ bot.get_channel()
        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
        # คำแนะนำ: เชื่อมต่อกับห้องเสียงโดยใช้ await
        voice_client = await voice_channel.connect()
        
        # ส่งชื่อข่าวที่กำลังอ่านไปยังห้องเสียง
        # คำแนะนำ: ส่งข้อความไปยังห้องเสียงพร้อมชื่อข่าว
        await voice_channel.send("กำลังเริ่มอ่านข่าว")
        # เล่นไฟล์เสียงในห้องเสียง
        # คำแนะนำ: ใช้ discord.FFmpegPCMAudio เพื่อสร้างแหล่งเสียงจากไฟล์
        voice_client.play(
            discord.FFmpegPCMAudio(temp_filename), 
            after=lambda e: asyncio.run_coroutine_threadsafe(
                cleanup(voice_client, temp_filename), bot.loop
            )
        )
    
    except Exception as e:
        # จัดการข้อผิดพลาดและส่งข้อความแจ้งเตือน
        # คำแนะนำ: ส่งข้อความพร้อมรายละเอียดข้อผิดพลาด
        await ctx.send("เครื่องค้างช่วยด้วยยย")
        # ลบไฟล์ชั่วคราวหากมีอยู่
        if temp_filename and os.path.exists(temp_filename):
            # คำแนะนำ: ใช้ os.unlink() เพื่อลบไฟล์
            os.unlink(temp_filename)

async def cleanup(voice_client, temp_filename):
    """ทำความสะอาดหลังจากเล่นเสียงเสร็จ"""
    # รอจนกว่าเสียงจะเล่นเสร็จ
    while voice_client.is_playing():
        await asyncio.sleep(0.5)
    
    # ตัดการเชื่อมต่อและลบไฟล์ชั่วคราว
    await voice_client.disconnect()
    if os.path.exists(temp_filename):
        os.unlink(temp_filename)

# รันบอท
bot.run(TOKEN) 