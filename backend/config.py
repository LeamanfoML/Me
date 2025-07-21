import os

# Конфигурация API
PORTALS_API_URL = "https://portals-market.com/api/v1/gifts"
TONNEL_API_URL = "https://market.tonnel.network/api/auctions"
PORTALS_API_KEY = os.getenv("PORTALS_API_KEY", "default_key")
TONNEL_API_KEY = os.getenv("TONNEL_API_KEY", "default_key")

# Комиссии (в TON)
PORTALS_FEE = 0.05  # 5%
TONNEL_FEE = 0.06   # 6%
TRANSFER_FEE = 0.22 # Комиссия перевода

# Telegram
BOT_TOKEN = "7807324480:AAEjLhfW0h6kkc7clCyWpkkBbU0uGdgaCiY"
ADMIN_CHAT_ID = "6284877635"

# Настройки обновления
UPDATE_INTERVAL = 30  # секунды
MIN_PROFIT = 0.1      # TON
