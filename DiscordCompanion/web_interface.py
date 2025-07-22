from flask import Flask, render_template, jsonify, request
from flask_migrate import Migrate
import requests
import os
from models import db
from database_utils import log_weather_query, get_popular_cities, get_recent_queries, get_total_stats

app = Flask(__name__)

# Configure Flask
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "discord-weather-bot-secret"

# Configure database
database_url = os.environ.get("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Create tables
with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# All Brazilian state capitals and major cities - same as bot
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

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/cities')
def get_cities():
    """API endpoint to get all available cities"""
    cities_list = []
    for key, value in cidades.items():
        cities_list.append({
            "id": key,
            "name": value["name"],
            "lat": value["lat"],
            "lon": value["lon"],
            "state": value.get("state", "BR")
        })
    return jsonify(cities_list)

@app.route('/api/weather/<city_id>')
def get_weather(city_id):
    """API endpoint to get weather for a specific city"""
    if city_id not in cidades:
        # Log failed query
        log_weather_query(
            city_id=city_id,
            city_name="Unknown",
            state=None,
            query_source='web',
            ip_address=request.remote_addr,
            success=False,
            error_message="City not found"
        )
        return jsonify({"error": "Cidade não encontrada"}), 404
    
    city_data = cidades[city_id]
    error_message = None
    temperature = None
    wind_speed = None
    success = False
    
    try:
        lat = city_data["lat"]
        lon = city_data["lon"]
        
        # Call Open-Meteo API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=America%2FSao_Paulo"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current_weather = data["current_weather"]
        temperature = current_weather["temperature"]
        wind_speed = current_weather.get("windspeed", 0)  # Open-Meteo uses 'windspeed' not 'wind_speed'
        success = True
        
        result = {
            "city": city_data["name"],
            "temperature": temperature,
            "wind_speed": wind_speed,
            "time": current_weather["time"],
            "success": True
        }
        
        # Log successful query
        log_weather_query(
            city_id=city_id,
            city_name=city_data["name"],
            state=city_data.get("state", "BR"),
            temperature=temperature,
            wind_speed=wind_speed,
            query_source='web',
            ip_address=request.remote_addr,
            success=True
        )
        
        return jsonify(result)
        
    except requests.exceptions.Timeout:
        error_message = "Timeout na API"
        result = {"error": error_message, "success": False}
    except requests.exceptions.RequestException:
        error_message = "Erro de rede"
        result = {"error": error_message, "success": False}
    except Exception as e:
        error_message = f"Erro interno: {str(e)}"
        result = {"error": "Erro interno", "success": False}
    
    # Log failed query
    log_weather_query(
        city_id=city_id,
        city_name=city_data["name"],
        state=city_data.get("state", "BR"),
        temperature=temperature,
        wind_speed=wind_speed,
        query_source='web',
        ip_address=request.remote_addr,
        success=False,
        error_message=error_message
    )
    
    return jsonify(result), 500

@app.route('/api/stats/popular-cities')
def get_popular_cities_api():
    """API endpoint to get most popular cities"""
    try:
        popular_cities = get_popular_cities(limit=10)
        return jsonify([city.to_dict() for city in popular_cities])
    except Exception as e:
        return jsonify({"error": "Failed to get popular cities"}), 500

@app.route('/api/stats/recent-queries')
def get_recent_queries_api():
    """API endpoint to get recent weather queries"""
    try:
        recent_queries = get_recent_queries(limit=20)
        return jsonify([query.to_dict() for query in recent_queries])
    except Exception as e:
        return jsonify({"error": "Failed to get recent queries"}), 500

@app.route('/api/stats/overview')
def get_stats_overview():
    """API endpoint to get overall statistics"""
    try:
        stats = get_total_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": "Failed to get statistics"}), 500

@app.route('/dashboard')
def dashboard():
    """Dashboard page with statistics"""
    return render_template('dashboard.html')

@app.route('/api/log-query', methods=['POST'])
def log_query_endpoint():
    """API endpoint to log weather queries from Discord bot"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        log_weather_query(
            city_id=data.get('city_id'),
            city_name=data.get('city_name'),
            state=data.get('state'),
            temperature=data.get('temperature'),
            wind_speed=data.get('wind_speed'),
            query_source=data.get('query_source', 'unknown'),
            user_id=data.get('user_id'),
            success=data.get('success', True),
            error_message=data.get('error_message')
        )
        return jsonify({"status": "logged"}), 200
    except Exception as e:
        print(f"Error logging query: {e}")
        return jsonify({"error": "Failed to log query"}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Discord Weather Bot Web Interface"})

if __name__ == '__main__':
    print("🌐 Iniciando interface web...")
    print("📍 Acesse: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
