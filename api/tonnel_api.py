import httpx
import logging
from config import Config
from datetime import datetime, timedelta
from models import NFTItem
from database import db
import time
from utils import validate_nft_data  # Импорт функции валидации

logger = logging.getLogger(__name__)

class TonnelAPI:
    def __init__(self):
        self.base_url = Config.TONNEL_API_URL
        self.tokens = self._load_tokens()
    
    def _load_tokens(self):
        """Загрузка токенов из базы данных"""
        tokens = db.get_token("tonnel")
        return {
            "access": tokens[0] if tokens else "",
            "refresh": tokens[1] if tokens else "",
            "expires_at": tokens[2] if tokens else 0
        }
    
    async def refresh_token(self):
        """Обновление токена доступа для Tonnel API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    Config.TOKEN_REFRESH_URLS["tonnel"],
                    json={"refresh_token": self.tokens["refresh"]}
                )
                response.raise_for_status()
                data = response.json()
                
                # Обновляем токены в базе
                expires_at = time.time() + data['expires_in']
                db.save_token(
                    "tonnel",
                    data['access_token'],
                    data['refresh_token'],
                    expires_at
                )
                self.tokens = {
                    "access": data['access_token'],
                    "refresh": data['refresh_token'],
                    "expires_at": expires_at
                }
                logger.info("Tonnel tokens refreshed successfully")
                return True
        except httpx.HTTPStatusError as e:
            logger.error(f"Token refresh failed: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Tonnel token refresh error: {e}")
        return False
    
    async def _make_request(self, endpoint, params=None):
        """
        Универсальный метод для выполнения запросов к API Tonnel
        с автоматическим обновлением токенов
        """
        try:
            # Проверяем срок действия токена
            if time.time() > self.tokens["expires_at"] - 60:
                logger.info("Tonnel token expired, refreshing...")
                if not await self.refresh_token():
                    return None
            
            headers = {"Authorization": f"Bearer {self.tokens['access']}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    params=params,
                    timeout=15.0
                )
                
                # Обработка 401 ошибки (неавторизован)
                if response.status_code == 401:
                    logger.warning("Received 401, refreshing token...")
                    if await self.refresh_token():
                        headers["Authorization"] = f"Bearer {self.tokens['access']}"
                        response = await client.get(
                            f"{self.base_url}{endpoint}",
                            headers=headers,
                            params=params,
                            timeout=15.0
                        )
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return None
    
    async def get_active_auctions(self, min_price=0, max_price=1000) -> list[NFTItem]:
        """
        Получение активных аукционов с фильтрацией по цене
        """
        params = {
            "status": "active",
            "min_price": min_price,
            "max_price": max_price,
            "limit": 100  # Ограничение количества результатов
        }
        
        data = await self._make_request("auctions", params)
        if not data or 'items' not in data:
            return []
        
        auctions = []
        for item in data['items']:
            # Валидация данных перед созданием объекта
            if not validate_nft_data(item):
                logger.warning(f"Invalid NFT data: {item}")
                continue
                
            try:
                auctions.append(NFTItem(
                    id=item['id'],
                    name=item['name'],
                    model=item.get('model', 'Unknown'),
                    current_bid=float(item['current_price']),
                    end_time=datetime.fromisoformat(item['end_time'].replace("Z", "")),
                    image_url=item.get('image_url', '')
                ))
            except (KeyError, ValueError, TypeError) as e:
                logger.error(f"Error parsing auction item: {e} | Data: {item}")
        
        return auctions
    
    async def get_market_listings(self, min_price=0, max_price=1000) -> dict[str, float]:
        """
        Получение текущих рыночных предложений с фильтрацией по цене
        """
        params = {
            "status": "listed",
            "min_price": min_price,
            "max_price": max_price,
            "limit": 200
        }
        
        data = await self._make_request("market/listings", params)
        if not data or 'items' not in data:
            return {}
        
        prices = {}
        for item in data['items']:
            try:
                # Используем ID NFT в качестве ключа
                nft_id = item['nft']['id']
                price = float(item['price'])
                prices[nft_id] = price
            except (KeyError, ValueError, TypeError) as e:
                logger.error(f"Error parsing market item: {e} | Data: {item}")
        
        return prices
    
    async def get_gift_details(self, gift_id: str) -> dict:
        """Получение детальной информации о подарке по ID"""
        return await self._make_request(f"gifts/{gift_id}")
