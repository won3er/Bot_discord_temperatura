import discord
from discord.ext import commands
import requests
import os

# Configure intents
intents = discord.Intents.default()
intents.message_content = True  # Enable bot to read message content

# Initialize bot
bot = commands.Bot(command_prefix="!", intents=intents)

# All Brazilian state capitals and major cities
cidades = {
    # Distrito Federal
    "brasilia": {"lat": -15.7939, "lon": -47.8828, "name": "Brasília", "state": "DF"},
    
    # Região Norte
    "rio_branco": {"lat": -9.9753, "lon": -67.8243, "name": "Rio Branco", "state": "AC"},
    "macapa": {"lat": 0.0389, "lon": -51.0664, "name": "Macapá", "state": "AP"},
    "manaus": {"lat": -3.1190, "lon": -60.0217, "name": "Manaus", "state": "AM"},
    "belem": {"lat": -1.4558, "lon": -48.5039, "name": "Belém", "state": "PA"},
    "porto_velho": {"lat": -8.7619, "lon": -63.9039, "name": "Porto Velho", "state": "RO"},
    "boa_vista": {"lat": 2.8197, "lon": -60.6733, "name": "Boa Vista", "state": "RR"},
    "palmas": {"lat": -10.2128, "lon": -48.3603, "name": "Palmas", "state": "TO"},
    
    # Região Nordeste
    "maceio": {"lat": -9.6658, "lon": -35.7350, "name": "Maceió", "state": "AL"},
    "salvador": {"lat": -12.9714, "lon": -38.5014, "name": "Salvador", "state": "BA"},
    "fortaleza": {"lat": -3.7319, "lon": -38.5267, "name": "Fortaleza", "state": "CE"},
    "sao_luis": {"lat": -2.5297, "lon": -44.3028, "name": "São Luís", "state": "MA"},
    "joao_pessoa": {"lat": -7.1195, "lon": -34.8450, "name": "João Pessoa", "state": "PB"},
    "recife": {"lat": -8.0476, "lon": -34.8770, "name": "Recife", "state": "PE"},
    "teresina": {"lat": -5.0892, "lon": -42.8019, "name": "Teresina", "state": "PI"},
    "natal": {"lat": -5.7945, "lon": -35.2110, "name": "Natal", "state": "RN"},
    "aracaju": {"lat": -10.9472, "lon": -37.0731, "name": "Aracaju", "state": "SE"},
    
    # Região Centro-Oeste
    "goiania": {"lat": -16.6864, "lon": -49.2643, "name": "Goiânia", "state": "GO"},
    "cuiaba": {"lat": -15.6014, "lon": -56.0979, "name": "Cuiabá", "state": "MT"},
    "campo_grande": {"lat": -20.4697, "lon": -54.6201, "name": "Campo Grande", "state": "MS"},
    
    # Região Sudeste
    "vitoria": {"lat": -20.3155, "lon": -40.3128, "name": "Vitória", "state": "ES"},
    "belo_horizonte": {"lat": -19.9167, "lon": -43.9345, "name": "Belo Horizonte", "state": "MG"},
    "rio_de_janeiro": {"lat": -22.9068, "lon": -43.1729, "name": "Rio de Janeiro", "state": "RJ"},
    "sao_paulo": {"lat": -23.5558, "lon": -46.6396, "name": "São Paulo", "state": "SP"},
    
    # Região Sul
    "curitiba": {"lat": -25.4284, "lon": -49.2733, "name": "Curitiba", "state": "PR"},
    "porto_alegre": {"lat": -30.0346, "lon": -51.2177, "name": "Porto Alegre", "state": "RS"},
    "florianopolis": {"lat": -27.5954, "lon": -48.5480, "name": "Florianópolis", "state": "SC"},
    
    # Cidades importantes adicionais
    "olinda": {"lat": -7.9986, "lon": -34.8417, "name": "Olinda", "state": "PE"},
    "campinas": {"lat": -22.9099, "lon": -47.0626, "name": "Campinas", "state": "SP"},
    "guarulhos": {"lat": -23.4538, "lon": -46.5333, "name": "Guarulhos", "state": "SP"},
    "sao_bernardo": {"lat": -23.6914, "lon": -46.5646, "name": "São Bernardo do Campo", "state": "SP"},
    "santo_andre": {"lat": -23.6528, "lon": -46.5311, "name": "Santo André", "state": "SP"},
    "osasco": {"lat": -23.5329, "lon": -46.7918, "name": "Osasco", "state": "SP"},
    "ribeirao_preto": {"lat": -21.1775, "lon": -47.8100, "name": "Ribeirão Preto", "state": "SP"},
    "sorocaba": {"lat": -23.5015, "lon": -47.4526, "name": "Sorocaba", "state": "SP"},
    "santos": {"lat": -23.9608, "lon": -46.3331, "name": "Santos", "state": "SP"},
    "nova_iguacu": {"lat": -22.7592, "lon": -43.4511, "name": "Nova Iguaçu", "state": "RJ"},
    "duque_de_caxias": {"lat": -22.7856, "lon": -43.3117, "name": "Duque de Caxias", "state": "RJ"},
    "niteroi": {"lat": -22.8833, "lon": -43.1036, "name": "Niterói", "state": "RJ"},
    "sao_goncalo": {"lat": -22.8267, "lon": -43.0533, "name": "São Gonçalo", "state": "RJ"},
    "contagem": {"lat": -19.9317, "lon": -44.0536, "name": "Contagem", "state": "MG"},
    "uberlandia": {"lat": -18.9113, "lon": -48.2622, "name": "Uberlândia", "state": "MG"},
    "juiz_de_fora": {"lat": -21.7587, "lon": -43.3496, "name": "Juiz de Fora", "state": "MG"},
    "londrina": {"lat": -23.3045, "lon": -51.1696, "name": "Londrina", "state": "PR"},
    "maringa": {"lat": -23.4205, "lon": -51.9331, "name": "Maringá", "state": "PR"},
    "joinville": {"lat": -26.3044, "lon": -48.8487, "name": "Joinville", "state": "SC"},
    "blumenau": {"lat": -26.9194, "lon": -49.0661, "name": "Blumenau", "state": "SC"},
    "caxias_do_sul": {"lat": -29.1678, "lon": -51.1794, "name": "Caxias do Sul", "state": "RS"},
    "pelotas": {"lat": -31.7654, "lon": -52.3376, "name": "Pelotas", "state": "RS"},
    "feira_de_santana": {"lat": -12.2664, "lon": -38.9663, "name": "Feira de Santana", "state": "BA"},
    "campina_grande": {"lat": -7.2306, "lon": -35.8811, "name": "Campina Grande", "state": "PB"},
    "caruaru": {"lat": -8.2836, "lon": -35.9761, "name": "Caruaru", "state": "PE"},
    "petrolina": {"lat": -9.3891, "lon": -40.5030, "name": "Petrolina", "state": "PE"},
    "juazeiro_do_norte": {"lat": -7.2031, "lon": -39.3144, "name": "Juazeiro do Norte", "state": "CE"},
    "sobral": {"lat": -3.6833, "lon": -40.3500, "name": "Sobral", "state": "CE"},
    "imperatriz": {"lat": -5.5267, "lon": -47.4917, "name": "Imperatriz", "state": "MA"},
    "parnamirim": {"lat": -5.9156, "lon": -35.2564, "name": "Parnamirim", "state": "RN"},
    "caucaia": {"lat": -3.7361, "lon": -38.6531, "name": "Caucaia", "state": "CE"}
}

@bot.event
async def on_ready():
    """Event triggered when bot comes online"""
    print(f"✅ Bot online como {bot.user}")
    print(f"📍 Conectado a {len(bot.guilds)} servidor(es)")
    
    # Set bot status
    activity = discord.Activity(type=discord.ActivityType.watching, name="!t <cidade> para clima")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Handle temperature command
    if message.content.startswith("!t"):
        cidade_input = message.content[2:].strip().lower().replace(" ", "_")
        
        # If no city provided, show help
        if not cidade_input:
            embed = discord.Embed(
                title="🌡️ Bot de Clima - Ajuda",
                description="Use `!t <cidade>` para obter a temperatura atual",
                color=0x3498db
            )
            embed.add_field(
                name="Cidades disponíveis:",
                value=", ".join([cidades[key]["name"] for key in sorted(cidades.keys())]),
                inline=False
            )
            embed.add_field(
                name="Exemplo:",
                value="`!t recife` ou `!t sao_paulo`",
                inline=False
            )
            await message.channel.send(embed=embed)
            return

        # Check if city exists
        if cidade_input in cidades:
            try:
                # Get coordinates
                lat = cidades[cidade_input]["lat"]
                lon = cidades[cidade_input]["lon"]
                city_name = cidades[cidade_input]["name"]

                # Call Open-Meteo API
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=America%2FSao_Paulo"
                
                print(f"🌐 Fazendo requisição para: {url}")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                # Extract weather data
                current_weather = data["current_weather"]
                temp = current_weather["temperature"]
                wind_speed = current_weather.get("windspeed", 0)  # Open-Meteo uses 'windspeed' not 'wind_speed'
                
                # Create rich embed response
                embed = discord.Embed(
                    title=f"🌡️ Clima em {city_name}",
                    color=0x27ae60 if temp > 20 else 0x3498db if temp > 10 else 0xe74c3c
                )
                
                embed.add_field(name="🌡️ Temperatura", value=f"{temp}°C", inline=True)
                embed.add_field(name="💨 Vento", value=f"{wind_speed} km/h", inline=True)
                embed.add_field(name="⏰ Atualizado", value="Agora", inline=True)
                
                # Add temperature emoji based on value
                if temp >= 30:
                    embed.set_footer(text="🔥 Está quente!")
                elif temp >= 20:
                    embed.set_footer(text="☀️ Temperatura agradável")
                elif temp >= 10:
                    embed.set_footer(text="🌤️ Está fresco")
                else:
                    embed.set_footer(text="🥶 Está frio!")
                
                await message.channel.send(embed=embed)
                
                # Log query to database (fire and forget)
                try:
                    log_data = {
                        'city_id': cidade_input,
                        'city_name': city_name,
                        'state': cidades[cidade_input].get("state", "BR"),
                        'temperature': temp,
                        'wind_speed': wind_speed,
                        'query_source': 'discord',
                        'user_id': str(message.author.id),
                        'success': True
                    }
                    requests.post('http://localhost:5000/api/log-query', json=log_data, timeout=1)
                except Exception:
                    pass  # Ignore logging errors
                
            except requests.exceptions.Timeout:
                await message.channel.send("⏰ **Timeout:** A API demorou muito para responder. Tente novamente.")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro de requisição: {e}")
                await message.channel.send("🌐 **Erro de rede:** Não foi possível conectar com o serviço de clima.")
                
            except KeyError as e:
                print(f"❌ Erro nos dados da API: {e}")
                await message.channel.send("📊 **Erro nos dados:** Resposta inesperada da API de clima.")
                
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                await message.channel.send("💥 **Erro inesperado:** Algo deu errado. Tente novamente mais tarde.")
        else:
            # City not found
            embed = discord.Embed(
                title="⚠️ Cidade não encontrada",
                description=f"A cidade `{cidade_input}` não está na nossa lista.",
                color=0xe67e22
            )
            embed.add_field(
                name="Cidades disponíveis:",
                value=", ".join([cidades[key]["name"] for key in sorted(cidades.keys())]),
                inline=False
            )
            await message.channel.send(embed=embed)

    # Process other commands
    await bot.process_commands(message)

@bot.command(name="cidades")
async def lista_cidades(ctx):
    """Command to list all available cities"""
    embed = discord.Embed(
        title="🏙️ Cidades Disponíveis",
        description="Lista de todas as cidades suportadas pelo bot:",
        color=0x9b59b6
    )
    
    cities_list = "\n".join([f"• {cidades[key]['name']} (`{key}`)" for key in sorted(cidades.keys())])
    embed.add_field(name="Cidades:", value=cities_list, inline=False)
    embed.add_field(name="Como usar:", value="`!t <cidade>` - Ex: `!t recife`", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="help")
async def help_command(ctx):
    """Custom help command"""
    embed = discord.Embed(
        title="🤖 Bot de Clima - Ajuda",
        description="Bot para consultar temperatura de cidades brasileiras",
        color=0x3498db
    )
    
    embed.add_field(
        name="📋 Comandos:",
        value="`!t <cidade>` - Mostra a temperatura\n`!cidades` - Lista cidades disponíveis\n`!help` - Mostra esta ajuda",
        inline=False
    )
    
    embed.add_field(
        name="🌡️ Exemplo de uso:",
        value="`!t recife`\n`!t sao_paulo`\n`!t rio_de_janeiro`",
        inline=False
    )
    
    embed.set_footer(text="Powered by Open-Meteo API")
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❓ Comando não encontrado",
            description="Use `!help` para ver os comandos disponíveis.",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
    else:
        print(f"❌ Erro de comando: {error}")
        await ctx.send("💥 **Erro:** Algo deu errado ao executar o comando.")

# Run the bot
if __name__ == "__main__":
    # Get token from environment variable
    token = os.getenv("DISCORD_BOT_TOKEN", "")
    
    if not token:
        print("❌ ERRO: Token do Discord não encontrado!")
        print("💡 Configure a variável de ambiente DISCORD_BOT_TOKEN")
        exit(1)
    
    try:
        print("🚀 Iniciando bot...")
        bot.run(token)
    except discord.LoginFailure:
        print("❌ ERRO: Token inválido!")
    except Exception as e:
        print(f"❌ ERRO: {e}")
