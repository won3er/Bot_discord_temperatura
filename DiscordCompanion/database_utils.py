from datetime import datetime, date, timedelta
from models import db, WeatherQuery, CityStats, BotStats
from sqlalchemy import func

def log_weather_query(city_id, city_name, state, temperature=None, wind_speed=None, 
                     query_source='web', user_id=None, ip_address=None, success=True, error_message=None):
    """Log a weather query to the database"""
    try:
        # Create weather query record
        query = WeatherQuery(
            city_id=city_id,
            city_name=city_name,
            state=state,
            temperature=temperature,
            wind_speed=wind_speed,
            query_source=query_source,
            user_id=user_id,
            ip_address=ip_address,
            success=success,
            error_message=error_message
        )
        db.session.add(query)
        
        # Update or create city statistics
        city_stat = CityStats.query.filter_by(city_id=city_id).first()
        if not city_stat:
            city_stat = CityStats(
                city_id=city_id,
                city_name=city_name,
                state=state,
                total_queries=0,
                discord_queries=0,
                web_queries=0
            )
            db.session.add(city_stat)
        
        # Update city stats
        city_stat.total_queries += 1
        city_stat.last_query = datetime.utcnow()
        
        if query_source == 'discord':
            city_stat.discord_queries += 1
        elif query_source == 'web':
            city_stat.web_queries += 1
        
        # Update temperature statistics if successful
        if success and temperature is not None:
            if city_stat.avg_temperature is None:
                city_stat.avg_temperature = temperature
                city_stat.min_temperature = temperature
                city_stat.max_temperature = temperature
            else:
                # Calculate new average
                total_temp_queries = WeatherQuery.query.filter_by(
                    city_id=city_id, success=True
                ).filter(WeatherQuery.temperature.isnot(None)).count()
                
                if total_temp_queries > 0:
                    city_stat.avg_temperature = (city_stat.avg_temperature * (total_temp_queries - 1) + temperature) / total_temp_queries
                    city_stat.min_temperature = min(city_stat.min_temperature, temperature)
                    city_stat.max_temperature = max(city_stat.max_temperature, temperature)
        
        # Update daily bot statistics
        today = date.today()
        bot_stat = BotStats.query.filter_by(date=today).first()
        if not bot_stat:
            bot_stat = BotStats(
                date=today,
                total_queries=0,
                discord_queries=0,
                web_queries=0,
                unique_cities=0,
                successful_queries=0,
                failed_queries=0
            )
            db.session.add(bot_stat)
        
        bot_stat.total_queries += 1
        if query_source == 'discord':
            bot_stat.discord_queries += 1
        elif query_source == 'web':
            bot_stat.web_queries += 1
        
        if success:
            bot_stat.successful_queries += 1
        else:
            bot_stat.failed_queries += 1
        
        # Update unique cities count for today
        unique_cities_today = db.session.query(func.count(func.distinct(WeatherQuery.city_id))).filter(
            func.date(WeatherQuery.timestamp) == today
        ).scalar()
        bot_stat.unique_cities = unique_cities_today
        
        db.session.commit()
        return query.id
        
    except Exception as e:
        db.session.rollback()
        print(f"Error logging weather query: {e}")
        return None

def get_popular_cities(limit=10):
    """Get most popular cities by query count"""
    return CityStats.query.order_by(CityStats.total_queries.desc()).limit(limit).all()

def get_recent_queries(limit=50):
    """Get recent weather queries"""
    return WeatherQuery.query.order_by(WeatherQuery.timestamp.desc()).limit(limit).all()

def get_city_statistics(city_id):
    """Get statistics for a specific city"""
    return CityStats.query.filter_by(city_id=city_id).first()

def get_daily_stats(days=7):
    """Get bot statistics for the last N days"""
    return BotStats.query.order_by(BotStats.date.desc()).limit(days).all()

def get_total_stats():
    """Get overall statistics"""
    total_queries = WeatherQuery.query.count()
    successful_queries = WeatherQuery.query.filter_by(success=True).count()
    unique_cities = db.session.query(func.count(func.distinct(WeatherQuery.city_id))).scalar()
    discord_queries = WeatherQuery.query.filter_by(query_source='discord').count()
    web_queries = WeatherQuery.query.filter_by(query_source='web').count()
    
    return {
        'total_queries': total_queries,
        'successful_queries': successful_queries,
        'failed_queries': total_queries - successful_queries,
        'unique_cities': unique_cities,
        'discord_queries': discord_queries,
        'web_queries': web_queries,
        'success_rate': (successful_queries / total_queries * 100) if total_queries > 0 else 0
    }

def cleanup_old_queries(days_to_keep=30):
    """Clean up old weather queries (keep only last N days)"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        old_queries = WeatherQuery.query.filter(WeatherQuery.timestamp < cutoff_date).count()
        
        if old_queries > 0:
            WeatherQuery.query.filter(WeatherQuery.timestamp < cutoff_date).delete()
            db.session.commit()
            print(f"Cleaned up {old_queries} old weather queries")
        
        return old_queries
    except Exception as e:
        db.session.rollback()
        print(f"Error cleaning up old queries: {e}")
        return 0