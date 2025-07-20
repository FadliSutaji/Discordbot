import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

API_KEY = ""  # ganti dengan API Key kamu

conversation_history = [
    {"role": "system", "content": "Kamu adalah asisten Discord."}
]

@bot.event
async def on_ready():
    print(f"✅ Bot aktif sebagai {bot.user}")

@bot.command()
async def tanya(ctx, *, pertanyaan):
    await ctx.send(f"{ctx.author.mention} 🤖 Nunggu jawaban dari AI...")
    conversation_history.append({"role": "user", "content": pertanyaan})
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://discord.com",
        "X-Title": "bot-discord-fadli"
    }

    data = {
        "model": "deepseek/deepseek-chat-v3-0324",
        "messages": [
            {"role": "user", "content": pertanyaan}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        print("✅ STATUS:", response.status_code)
        print("✅ RESPONSE:", response.text)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            jawaban = result["choices"][0]["message"]["content"]
            await ctx.send(f"{ctx.author.mention} {jawaban}")
            conversation_history.append({"role": "user", "content": pertanyaan})
        else:
            await ctx.send(f"{ctx.author.mention} ❌ AI gak ngasih jawaban.")
        
    except requests.exceptions.HTTPError as http_err:
        await ctx.send(f"{ctx.author.mention} ❌ HTTP error: {http_err}")
        print("❌ HTTP ERROR:", http_err)
    except Exception as e:
        await ctx.send(f"{ctx.author.mention} ❌ Gagal ambil jawaban dari AI.")
        print("❌ ERROR:", e)

bot.run("")  # token bot discord kamu
