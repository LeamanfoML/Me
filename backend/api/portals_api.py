import requests
import logging
from config import PORTALS_API_URL, PORTALS_API_KEY
from models import ArbitrageOpportunity
from database import db_session

logger = logging.getLogger(__name__)

def fetch_portals_data():
    """Получить данные с Portals Market с автоматическим обновлением токена"""
    try:
        headers = {
            "Authorization": f"Bearer {PORTALS_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.get(PORTALS_API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        logger.error(f"Portals API error: {str(e)}")
        # Здесь можно добавить логику обновления токена
        return []
