// Инициализация Telegram WebApp
const tg = window.Telegram.WebApp;
tg.expand();
tg.enableClosingConfirmation();
tg.MainButton.setText("ЗАКРЫТЬ").show();

// Элементы DOM
const refreshBtn = document.getElementById('refreshBtn');
const autoRefreshToggle = document.getElementById('autoRefreshToggle');
const sortSelect = document.getElementById('sortSelect');
const minProfitInput = document.getElementById('minProfit');
const maxPriceInput = document.getElementById('maxPrice');
const applyFiltersBtn = document.getElementById('applyFilters');
const opportunitiesList = document.getElementById('opportunitiesList');
const lastUpdateSpan = document.getElementById('lastUpdate');
const totalOpportunitiesSpan = document.getElementById('totalOpportunities');

// Конфигурация
const API_URL = "https://your-domain.com/api"; // Заменить на реальный URL
let autoRefreshInterval;
let currentFilters = {
    minProfit: 0.1,
    maxPrice: 100,
    sortBy: 'profit_desc'
};

// Инициализация приложения
function initApp() {
    loadOpportunities();
    setupEventListeners();
    startAutoRefresh();
}

// Настройка обработчиков событий
function setupEventListeners() {
    refreshBtn.addEventListener('click', loadOpportunities);
    applyFiltersBtn.addEventListener('click', applyFilters);
    sortSelect.addEventListener('change', () => {
        currentFilters.sortBy = sortSelect.value;
        loadOpportunities();
    });
    autoRefreshToggle.addEventListener('change', toggleAutoRefresh);
    tg.MainButton.onClick(() => tg.close());
}

// Загрузить арбитражные возможности
async function loadOpportunities() {
    try {
        tg.showProgressBar();
        
        const params = new URLSearchParams({
            min_profit: currentFilters.minProfit,
            max_price: currentFilters.maxPrice,
            sort_by: currentFilters.sortBy
        });
        
        const response = await fetch(`${API_URL}/opportunities?${params}`);
        const data = await response.json();
        
        if (data.success) {
            renderOpportunities(data.data);
            updateStats(data.data.length);
        } else {
            tg.showAlert(`Ошибка: ${data.error}`);
        }
    } catch (error) {
        tg.showAlert(`Сетевая ошибка: ${error.message}`);
    } finally {
        tg.hideProgressBar();
    }
}

// Отобразить возможности
function renderOpportunities(opportunities) {
    opportunitiesList.innerHTML = '';
    
    if (opportunities.length === 0) {
        opportunitiesList.innerHTML = '<p class="no-data">🚫 Арбитражные возможности не найдены</p>';
        return;
    }
    
    opportunities.forEach(opp => {
        const card = document.createElement('div');
        card.className = 'opportunity-card';
        
        card.innerHTML = `
            <div class="card-header">
                <div class="gift-name">${opp.gift_name}</div>
                <div class="model">${opp.model}</div>
            </div>
            
            <div class="prices">
                <div class="price-item">
                    <div class="price-label">Аукцион</div>
                    <div class="price-value">${opp.auction_price} TON</div>
                </div>
                <div class="price-item">
                    <div class="price-label">Portals</div>
                    <div class="price-value">${opp.portals_price} TON</div>
                </div>
                <div class="price-item">
                    <div class="price-label">Tonnel</div>
                    <div class="price-value">${opp.tonnel_price} TON</div>
                </div>
            </div>
            
            <div class="profit ${opp.profit > 0 ? 'positive' : ''}">
                ${opp.profit > 0 ? '+' : ''}${opp.profit.toFixed(2)} TON
            </div>
            
            <div class="auction-time">
                <span>${opp.marketplace}</span>
                <span>Окончание: ${formatTime(opp.auction_end_time)}</span>
            </div>
        `;
        
        opportunitiesList.appendChild(card);
    });
}

// Применить фильтры
function applyFilters() {
    currentFilters.minProfit = parseFloat(minProfitInput.value) || 0.1;
    currentFilters.maxPrice = parseFloat(maxPriceInput.value) || 100;
    loadOpportunities();
}

// Обновить статистику
function updateStats(count) {
    totalOpportunitiesSpan.textContent = count;
    lastUpdateSpan.textContent = new Date().toLocaleTimeString();
}

// Автоматическое обновление
function startAutoRefresh() {
    if (autoRefreshInterval) clearInterval(autoRefreshInterval);
    autoRefreshInterval = setInterval(loadOpportunities, 10000);
}

function toggleAutoRefresh() {
    if (autoRefreshToggle.checked) {
        startAutoRefresh();
    } else {
        clearInterval(autoRefreshInterval);
    }
}

// Вспомогательные функции
function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Запустить приложение
document.addEventListener('DOMContentLoaded', initApp);
