# Discord Weather Bot

## Overview

A Discord bot application that provides weather information for Brazilian cities using the Open-Meteo API. The application consists of a Discord bot with Portuguese commands and a complementary web interface built with Flask. It supports all 27 Brazilian state capitals plus 30+ major cities (60+ total), providing real-time weather data through both Discord commands and a responsive web interface with regional organization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Web Interface**: HTML5 with Bootstrap 5 for responsive design
- **Interactive Elements**: Vanilla JavaScript (ES6) with Bootstrap components
- **Styling**: Custom CSS with CSS variables for theming and responsive design
- **UI Components**: Cards, modals, alerts, and interactive city selection

### Backend Architecture
- **Discord Bot**: Built with discord.py library using command prefix "!"
- **Web Server**: Flask application serving both API endpoints and static content
- **API Structure**: RESTful endpoints for city data and weather information
- **Event-Driven**: Discord bot uses event handlers for message processing

### Data Management
- **Static Data**: Hardcoded city coordinates and information in Python dictionaries
- **External API**: Open-Meteo weather API for real-time temperature data
- **PostgreSQL Database**: Stores query logs, city statistics, and usage analytics
- **Analytics**: Tracks popular cities, success rates, and usage patterns

## Key Components

### Discord Bot (bot.py)
- **Purpose**: Main Discord bot with weather commands
- **Commands**: 
  - `!t <cidade>` - Get temperature for a city
  - `!cidades` - List all supported cities
  - `!help` - Show command help
- **Features**: Rich embeds, error handling, Portuguese language support

### Web Interface (web_interface.py + HTML/CSS/JS)
- **Purpose**: Alternative web-based interface for weather queries with analytics dashboard
- **Flask Routes**: 
  - `/` - Main interface page
  - `/dashboard` - Analytics dashboard with statistics
  - `/api/cities` - Get all cities data
  - `/api/weather/<city_id>` - Get weather for specific city
  - `/api/log-query` - Log weather queries from Discord bot
  - `/api/stats/*` - Various statistics endpoints
- **Frontend**: Bootstrap-based responsive design with interactive city grid and analytics dashboard

### Database Layer (models.py + database_utils.py)
- **WeatherQuery Model**: Tracks individual weather queries with temperature, success status, source (Discord/Web)
- **CityStats Model**: Aggregates statistics per city including query counts, temperature ranges
- **BotStats Model**: Daily usage statistics and success rates
- **Analytics Functions**: Popular cities, recent queries, total statistics, and data cleanup utilities

### City Data Structure
- **60+ Brazilian Cities**: All 27 state capitals plus major metropolitan cities
- **Regional Organization**: Cities grouped by Brazilian regions (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)
- **Comprehensive Coverage**: Includes all capitals and important cities from São Paulo, Rio de Janeiro, Minas Gerais, and other major states
- **Coordinate Storage**: Latitude and longitude for each city with WGS84 datum
- **State Information**: Each city includes state abbreviation for better organization
- **Consistent Naming**: Standardized city identifiers across bot and web interface

## Data Flow

1. **User Input**: 
   - Discord: User sends `!t <cidade>` command
   - Web: User selects city from dropdown or clicks city card

2. **City Resolution**:
   - Input normalized (lowercase, spaces to underscores)
   - City lookup in predefined dictionary
   - Coordinate extraction for API call

3. **Weather API Call**:
   - HTTP request to Open-Meteo API with coordinates
   - Real-time temperature data retrieval
   - Error handling for API failures

4. **Response Formatting**:
   - Discord: Rich embed with temperature and city name
   - Web: JSON response with temperature data and city information

5. **User Display**:
   - Discord: Formatted message in channel
   - Web: Dynamic UI update with weather information

## External Dependencies

### APIs
- **Open-Meteo API**: Free weather API providing current temperature data
- **Discord API**: Bot authentication and message handling

### Python Libraries
- **discord.py**: Discord bot framework with intents support
- **Flask**: Web framework for API and interface
- **requests**: HTTP client for external API calls

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI enhancement

## Deployment Strategy

### Environment Configuration
- **Required Environment Variable**: `DISCORD_BOT_TOKEN`
- **Bot Permissions**: Message content intent required for command processing
- **Flask Configuration**: Development mode with debug capabilities

### Running the Application
- **Discord Bot**: Run `bot.py` with valid Discord token
- **Web Interface**: Run `web_interface.py` to start Flask development server
- **Dual Mode**: Both components can run independently or simultaneously

### Scalability Considerations
- **Stateless Design**: No persistent data storage required
- **API Rate Limits**: Open-Meteo provides generous free tier
- **Error Handling**: Robust error handling for API failures and invalid inputs

The application is designed for easy deployment on platforms like Replit, with minimal configuration requirements and no database dependencies.