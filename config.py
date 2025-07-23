import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Основные настройки бота
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
    
    # Настройки API
    PORTALS_API_URL = "https://api.portals-market.com/v1/"
    TONNEL_API_URL = "https://api.market.tonnel.network/v1/"
    
    # Комиссии
    PORTALS_FEE = 0.05  # 5%
    TONNEL_FEE = 0.06   # 6%
    TRANSFER_FEE = 0.22  # TON
    
    # Параметры арбитража
    MIN_PROFIT = 0.1    # Минимальная прибыль в TON
    UPDATE_INTERVAL = 45  # Интервал обновления в секундах
    MANUAL_UPDATE_COOLDOWN = 10  # КД для ручного обновления
    
    # Настройки базы данных
    DB_NAME = "arbitrage_db.sqlite"
    
    # Пути для обновления токенов
    TOKEN_REFRESH_URLS = {
        "portals": "https://portals-market.com/api/auth/refresh",
        "tonnel": "https://market.tonnel.network/api/auth/refresh"
    }

config = Config()
