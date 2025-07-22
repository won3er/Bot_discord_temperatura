class WeatherBot {
    constructor() {
        this.cities = [];
        this.loadingModal = null;
        this.init();
    }

    async init() {
        // Initialize Bootstrap modal
        this.loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        
        // Load cities and set up event listeners
        await this.loadCities();
        this.setupEventListeners();
        this.loadCitiesGrid();
    }

    async loadCities() {
        try {
            const response = await fetch('/api/cities');
            if (!response.ok) throw new Error('Failed to load cities');
            
            this.cities = await response.json();
            this.populateCitySelect();
        } catch (error) {
            console.error('Error loading cities:', error);
            this.showAlert('Erro ao carregar cidades', 'danger');
        }
    }

    populateCitySelect() {
        const select = document.getElementById('citySelect');
        const getWeatherBtn = document.getElementById('getWeatherBtn');
        
        // Clear existing options
        select.innerHTML = '<option value="">Selecione uma cidade...</option>';
        
        // Add cities sorted by name
        this.cities
            .sort((a, b) => a.name.localeCompare(b.name))
            .forEach(city => {
                const option = document.createElement('option');
                option.value = city.id;
                option.textContent = city.name;
                select.appendChild(option);
            });
        
        // Enable the button
        getWeatherBtn.disabled = false;
    }

    setupEventListeners() {
        const getWeatherBtn = document.getElementById('getWeatherBtn');
        const citySelect = document.getElementById('citySelect');
        
        getWeatherBtn.addEventListener('click', () => {
            const selectedCity = citySelect.value;
            if (selectedCity) {
                this.getWeather(selectedCity);
            }
        });
        
        citySelect.addEventListener('change', () => {
            getWeatherBtn.disabled = !citySelect.value;
        });

        // Allow Enter key to trigger weather fetch
        citySelect.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && citySelect.value) {
                this.getWeather(citySelect.value);
            }
        });
    }

    async getWeather(cityId) {
        try {
            this.showLoading(true);
            
            const response = await fetch(`/api/weather/${cityId}`);
            const data = await response.json();
            
            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Failed to get weather data');
            }
            
            this.displayWeather(data);
            
        } catch (error) {
            console.error('Error getting weather:', error);
            this.showAlert(`Erro ao obter clima: ${error.message}`, 'danger');
        } finally {
            this.showLoading(false);
        }
    }

    displayWeather(data) {
        const resultDiv = document.getElementById('weatherResult');
        const contentDiv = document.getElementById('weatherContent');
        
        // Determine temperature category for styling
        const temp = data.temperature;
        let tempClass = 'cold';
        let tempIcon = 'fas fa-snowflake';
        let tempMessage = 'Está frio!';
        
        if (temp >= 30) {
            tempClass = 'hot';
            tempIcon = 'fas fa-fire';
            tempMessage = 'Está quente!';
        } else if (temp >= 20) {
            tempClass = 'warm';
            tempIcon = 'fas fa-sun';
            tempMessage = 'Temperatura agradável';
        } else if (temp >= 10) {
            tempClass = '';
            tempIcon = 'fas fa-cloud-sun';
            tempMessage = 'Está fresco';
        }
        
        contentDiv.innerHTML = `
            <div class="weather-display ${tempClass}">
                <div class="weather-icon">
                    <i class="${tempIcon}"></i>
                </div>
                <h2 class="city-name mb-3">${data.city}</h2>
                <div class="temperature-big mb-3">${temp}°C</div>
                <div class="row text-center">
                    <div class="col-6">
                        <i class="fas fa-wind me-2"></i>
                        <strong>Vento:</strong> ${data.wind_speed} km/h
                    </div>
                    <div class="col-6">
                        <i class="fas fa-clock me-2"></i>
                        <strong>Atualizado:</strong> Agora
                    </div>
                </div>
                <div class="mt-3">
                    <small>${tempMessage}</small>
                </div>
            </div>
        `;
        
        // Show result with animation
        resultDiv.style.display = 'block';
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    loadCitiesGrid() {
        const gridDiv = document.getElementById('citiesGrid');
        
        if (this.cities.length === 0) {
            gridDiv.innerHTML = '<div class="col-12 text-center">Carregando cidades...</div>';
            return;
        }
        
        gridDiv.innerHTML = '';
        
        // Group cities by region for better organization
        const regions = {
            'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
            'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
            'Centro-Oeste': ['GO', 'MT', 'MS', 'DF'],
            'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
            'Sul': ['PR', 'RS', 'SC']
        };

        const getRegion = (state) => {
            for (const [region, states] of Object.entries(regions)) {
                if (states.includes(state)) return region;
            }
            return 'Outras';
        };

        // Sort cities by region, then by name
        const sortedCities = this.cities.sort((a, b) => {
            const regionA = getRegion(a.state);
            const regionB = getRegion(b.state);
            if (regionA !== regionB) {
                const regionOrder = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul', 'Outras'];
                return regionOrder.indexOf(regionA) - regionOrder.indexOf(regionB);
            }
            return a.name.localeCompare(b.name);
        });

        sortedCities.forEach((city, index) => {
            const prevCity = sortedCities[index - 1];
            const currentRegion = getRegion(city.state);
            const prevRegion = prevCity ? getRegion(prevCity.state) : null;

            // Add region header if this is the first city of a new region
            if (currentRegion !== prevRegion) {
                const regionHeader = document.createElement('div');
                regionHeader.className = 'col-12 mt-4 mb-2';
                regionHeader.innerHTML = `
                    <h6 class="text-primary border-bottom pb-2 mb-0">
                        <i class="fas fa-map-marked-alt me-2"></i>
                        Região ${currentRegion}
                    </h6>
                `;
                gridDiv.appendChild(regionHeader);
            }

            const cityCard = document.createElement('div');
            cityCard.className = 'col-md-3 col-lg-2 mb-3';
            
            cityCard.innerHTML = `
                <div class="city-card p-3 h-100 d-flex flex-column justify-content-center text-center" 
                     onclick="weatherBot.selectCityAndGetWeather('${city.id}')"
                     data-city-id="${city.id}">
                    <h6 class="mb-2">${city.name}</h6>
                    <small class="text-muted mb-1">
                        <i class="fas fa-map me-1"></i>
                        ${city.state || 'BR'}
                    </small>
                    <small class="mt-2 text-primary">
                        <i class="fas fa-thermometer-half me-1"></i>
                        Clique para clima
                    </small>
                </div>
            `;
            
            gridDiv.appendChild(cityCard);
        });
    }

    selectCityAndGetWeather(cityId) {
        const citySelect = document.getElementById('citySelect');
        citySelect.value = cityId;
        
        // Add loading state to city card
        const cityCard = document.querySelector(`[data-city-id="${cityId}"]`);
        if (cityCard) {
            cityCard.classList.add('loading');
        }
        
        this.getWeather(cityId).finally(() => {
            if (cityCard) {
                cityCard.classList.remove('loading');
            }
        });
    }

    showLoading(show) {
        if (show) {
            this.loadingModal.show();
        } else {
            this.loadingModal.hide();
        }
    }

    showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-custom alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at top of container
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the weather bot when page loads
let weatherBot;
document.addEventListener('DOMContentLoaded', () => {
    weatherBot = new WeatherBot();
});

// Add some utility functions for better UX
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to get weather
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const citySelect = document.getElementById('citySelect');
            if (citySelect.value) {
                weatherBot.getWeather(citySelect.value);
            }
        }
    });
});
