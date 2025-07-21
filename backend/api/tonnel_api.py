import requests
import logging
from config import TONNEL_API_URL, TONNEL_API_KEY
from models import ArbitrageOpportunity
from database import db_session

logger = logging.getLogger(__name__)

def fetch_tonnel_data():
    """Получить аукционные данные с Tonnel"""
    try:
        params = {"status": "active", "limit": 100}
        headers = {"X-Api-Key": TONNEL_API_KEY}
        response = requests.get(TONNEL_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()['auctions']
    except requests.exceptions.RequestException as e:
        logger.error(f"Tonnel API error: {str(e)}")
        # Логика обновления токена
        return []
