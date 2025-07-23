import asyncio
import logging
from config import Config
from database import db
from api.portals_api import PortalsAPI
from api.tonnel_api import TonnelAPI
from services.arbitrage import ArbitrageCalculator

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        self.portals_api = PortalsAPI()
        self.tonnel_api = TonnelAPI()  # Аналогично PortalsAPI
        self.arbitrage = ArbitrageCalculator()
        self.is_running = True
    
    async def start(self):
        while self.is_running:
            try:
                await self.update_data()
                await asyncio.sleep(Config.UPDATE_INTERVAL)
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)  # Пауза при ошибке
    
    async def update_data(self):
        # Получаем данные с обоих маркетплейсов
        portals_auctions = await self.portals_api.get_active_auctions()
        tonnel_auctions = await self.tonnel_api.get_active_auctions()
        
        portals_prices = await self.portals_api.get_market_prices()
        tonnel_prices = await self.tonnel_api.get_market_prices()
        
        # Обогащаем данные ценами
        for item in portals_auctions:
            item.tonnel_price = tonnel_prices.get(item.id, 0)
        
        for item in tonnel_auctions:
            item.portals_price = portals_prices.get(item.id, 0)
        
        # Объединяем все аукционы
        all_items = portals_auctions + tonnel_auctions
        
        # Рассчитываем арбитраж
        results = []
        for item in all_items:
            result = self.arbitrage.calculate_profit(item)
            results.append(result)
        
        # Фильтруем и сортируем
        filtered = self.arbitrage.filter_opportunities(results)
        sorted_results = self.arbitrage.sort_by_profit(filtered)
        
        # Сохраняем в БД и отправляем уведомления
        for result in sorted_results:
            db.save_arbitrage_result(result)
            await self.send_notification(result)
    
    async def send_notification(self, result: 'ArbitrageResult'):
        message = self.format_message(result)
        try:
            await self.bot.send_message(
                chat_id=Config.ADMIN_CHAT_ID,
                text=message,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Notification send failed: {e}")
    
    def format_message(self, result) -> str:
        item = result.item
        return f"""
<b>💰 Арбитражная возможность!</b>
🎁 {item.name} ({item.model})
⏱ Окончание: {item.end_time.strftime('%d.%m %H:%M')}
        
📊 Цены:
├ Текущая ставка: {item.current_bid} TON
├ Portals Market: {item.portals_price} TON
└ Tonnel Market: {item.tonnel_price} TON
        
💵 Прибыль: <b>{result.profit} TON</b>
🔀 Действие: {result.action.replace('_', ' ').title()}
        """
