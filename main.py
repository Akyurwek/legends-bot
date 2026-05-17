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
    print(f"Bot başarıyla aktif oldu: {bot.user}")

@bot.command()
async def sor(ctx, *, soru):
    await ctx.send("Düşünüyorum aga, bekle...")
    try:
        response = model.generate_content(soru)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"Bir hata oluştu aga: {e}")

bot.run(DISCORD_TOKEN)
