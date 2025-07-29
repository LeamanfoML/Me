# utils.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

PORTALS_API_URL = os.getenv('PORTALS_API_URL')
TONNEL_API_URL = os.getenv('TONNEL_API_URL')
MRKT_API_URL = os.getenv('MRKT_API_URL')

# Получение данных с API маркетплейсов
def fetch_market_data(market_name):
    if market_name == 'portals':
        response = requests.get(PORTALS_API_URL)
    elif market_name == 'tonnel':
        response = requests.get(TONNEL_API_URL)
    elif market_name == 'mrkt':
        response = requests.get(MRKT_API_URL)
    else:
        return []

    if response.status_code == 200:
        return response.json()
    else:
        return []

# Расчет прибыли
def calculate_profit(gift, portals_data, tonnel_data, mrkt_data):
    portals_price = gift['portals_price']
    tonnel_price = gift['tonnel_price']
    mrkt_price = gift['mrkt_price']

    # Учет комиссий
    portals_commission = portals_price * 0.05
    tonnel_commission = tonnel_price * 0.06
    mrkt_commission = mrkt_price * 0.02
    transfer_commission = 0.22  # Комиссия перевода между маркетплейсами

    # Расчет прибыли
    profit_portals_to_tonnel = (tonnel_price - portals_price - portals_commission - tonnel_commission - transfer_commission)
    profit_portals_to_mrkt = (mrkt_price - portals_price - portals_commission - mrkt_commission - transfer_commission)
    profit_tonnel_to_portals = (portals_price - tonnel_price - tonnel_commission - portals_commission - transfer_commission)
    profit_tonnel_to_mrkt = (mrkt_price - tonnel_price - tonnel_commission - mrkt_commission - transfer_commission)
    profit_mrkt_to_portals = (portals_price - mrkt_price - mrkt_commission - portals_commission - transfer_commission)
    profit_mrkt_to_tonnel = (tonnel_price - mrkt_price - mrkt_commission - tonnel_commission - transfer_commission)

    # Выбор максимальной прибыли
    return max(profit_portals_to_tonnel, profit_portals_to_mrkt, 
               profit_tonnel_to_portals, profit_tonnel_to_mrkt, 
               profit_mrkt_to_portals, profit_mrkt_to_tonnel)

# Обновление токенов API
def update_tokens():
    # Здесь можно добавить логику для автоматического обновления токенов
    pass
