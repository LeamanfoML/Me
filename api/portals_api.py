import httpx
import logging
from config import Config
from datetime import datetime, timedelta
from models import NFTItem
from database import db
import time

logger = logging.getLogger(__name__)

class PortalsAPI:
    def __init__(self):
        self.base_url = Config.PORTALS_API_URL
        self.tokens = self._load_tokens()
    
    def _load_tokens(self):
        tokens = db.get_token("portals")
        return {
            "access": tokens[0] if tokens else "",
            "refresh": tokens[1] if tokens else "",
            "expires_at": tokens[2] if tokens else 0
        }
    
    async def refresh_token(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    Config.TOKEN_REFRESH_URLS["portals"],
                    json={"refresh_token": self.tokens["refresh"]}
                )
                response.raise_for_status()
                data = response.json()
                
                # Обновляем токены в базе
                expires_at = time.time() + data['expires_in']
                db.save_token(
                    "portals",
                    data['access_token'],
                    data['refresh_token'],
                    expires_at
                )
                self.tokens = {
                    "access": data['access_token'],
                    "refresh": data['refresh_token'],
                    "expires_at": expires_at
                }
                return True
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            return False
    
    async def _make_request(self, endpoint):
        try:
            # Проверяем срок действия токена
            if time.time() > self.tokens["expires_at"] - 60:
                await self.refresh_token()
            
            headers = {"Authorization": f"Bearer {self.tokens['access']}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 401:
                    await self.refresh_token()
                    headers["Authorization"] = f"Bearer {self.tokens['access']}"
                    response = await client.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers,
                        timeout=10.0
                    )
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Request failed: {e}")
        return None
    
    async def get_active_auctions(self) -> list[NFTItem]:
        data = await self._make_request("auctions/active")
        if not data:
            return []
        
        auctions = []
        for item in data['items']:
            auctions.append(NFTItem(
                id=item['id'],
                name=item['name'],
                model=item['model'],
                current_bid=float(item['current_bid']),
                end_time=datetime.fromisoformat(item['end_time']),
                image_url=item['image_url']
            ))
        return auctions
    
    async def get_market_prices(self) -> dict[str, float]:
        data = await self._make_request("market/prices")
        return {item['id']: float(item['price']) for item in data['items']}
