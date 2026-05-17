import os
import discord
from discord.ext import commands
import google.generativeai as genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot başarıyla aktif oldu: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or message.content.startswith("!sor "):
        ctx = await bot.get_context(message)
        soru = message.content.replace(f"<@{bot.user.id}>", "").replace("!sor ", "").strip()
        
        if not soru:
            await message.reply("Aga soruyu unuttun, ne sormak istiyorsun?")
            return
            
        async with ctx.typing():
            try:
                response = model.generate_content(soru)
                await message.reply(response.text[:1950])
            except Exception as e:
                print(f"Hata oluştu: {e}")
                await message.reply("Kafam karıştı aga, bir sorun olabilir.")
                
    await bot.process_commands(message)
import asyncio

async def main():
    async with bot:
        await bot.start(DISCORD_TOKEN)

try:
    asyncio.run(main())
except Exception as e:
    print(f"HATA CIKTI AGA: {e}")
