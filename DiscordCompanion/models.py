from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class WeatherQuery(db.Model):
    """Model to track weather queries and statistics"""
    __tablename__ = 'weather_queries'
    
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.String(50), nullable=False, index=True)
    city_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(5), nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    query_source = db.Column(db.String(20), nullable=False)  # 'discord' or 'web'
    user_id = db.Column(db.String(100), nullable=True)  # Discord user ID for bot queries
    ip_address = db.Column(db.String(45), nullable=True)  # IP for web queries
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    success = db.Column(db.Boolean, default=True, nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<WeatherQuery {self.city_name} at {self.timestamp}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'city_id': self.city_id,
            'city_name': self.city_name,
            'state': self.state,
            'temperature': self.temperature,
            'wind_speed': self.wind_speed,
            'query_source': self.query_source,
            'timestamp': self.timestamp.isoformat(),
            'success': self.success
        }

class CityStats(db.Model):
    """Model to track city popularity and statistics"""
    __tablename__ = 'city_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    city_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(5), nullable=True)
    total_queries = db.Column(db.Integer, default=0, nullable=False)
    discord_queries = db.Column(db.Integer, default=0, nullable=False)
    web_queries = db.Column(db.Integer, default=0, nullable=False)
    last_query = db.Column(db.DateTime, nullable=True)
    avg_temperature = db.Column(db.Float, nullable=True)
    min_temperature = db.Column(db.Float, nullable=True)
    max_temperature = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<CityStats {self.city_name} - {self.total_queries} queries>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'city_id': self.city_id,
            'city_name': self.city_name,
            'state': self.state,
            'total_queries': self.total_queries,
            'discord_queries': self.discord_queries,
            'web_queries': self.web_queries,
            'last_query': self.last_query.isoformat() if self.last_query else None,
            'avg_temperature': self.avg_temperature,
            'min_temperature': self.min_temperature,
            'max_temperature': self.max_temperature
        }

class BotStats(db.Model):
    """Model to track overall bot usage statistics"""
    __tablename__ = 'bot_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False, index=True)
    total_queries = db.Column(db.Integer, default=0, nullable=False)
    discord_queries = db.Column(db.Integer, default=0, nullable=False)
    web_queries = db.Column(db.Integer, default=0, nullable=False)
    unique_cities = db.Column(db.Integer, default=0, nullable=False)
    successful_queries = db.Column(db.Integer, default=0, nullable=False)
    failed_queries = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<BotStats {self.date} - {self.total_queries} queries>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'total_queries': self.total_queries,
            'discord_queries': self.discord_queries,
            'web_queries': self.web_queries,
            'unique_cities': self.unique_cities,
            'successful_queries': self.successful_queries,
            'failed_queries': self.failed_queries
        }