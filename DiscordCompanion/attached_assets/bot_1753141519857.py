import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True  # Habilita o bot para ler o conteúdo das mensagens

bot = commands.Bot(command_prefix="!", intents=intents)

cidades = {
    "recife": {"lat": -8.05, "lon": -34.9},
    "olinda": {"lat": -7.9986, "lon": -34.8417},
    "sao_paulo": {"lat": -23.5505, "lon": -46.6333},
    "rio_de_janeiro": {"lat": -22.9068, "lon": -43.1729},
    "brasilia": {"lat": -15.7939, "lon": -47.8828},
    "salvador": {"lat": -12.9777, "lon": -38.5016},
    "porto_alegre": {"lat": -30.0346, "lon": -51.2177},
    "fortaleza": {"lat": -3.7172, "lon": -38.5433},
    "manaus": {"lat": -3.1190, "lon": -60.0217},
    "belo_horizonte": {"lat": -19.9167, "lon": -43.9345}
}

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("!t"):
        cidade_input = message.content[2:].lower()

        if cidade_input in cidades:
            lat = cidades[cidade_input]["lat"]
            lon = cidades[cidade_input]["lon"]

            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            resposta = requests.get(url).json()

            try:
                temp = resposta["current_weather"]["temperature"]
                await message.channel.send(f"🌡️ Temperatura agora em **{cidade_input.replace('_', ' ').title()}**: `{temp}°C`")
            except Exception as e:
                print("Erro ao pegar temperatura:", e)
                await message.channel.send("❌ Erro ao obter a temperatura.")
        else:
            await message.channel.send("⚠️ Cidade não encontrada. Use nomes como `recife`, `olinda`, `sao_paulo`, etc.")

    await bot.process_commands(message)

# Cole seu token aqui:
bot.run("")

