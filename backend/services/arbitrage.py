from config import PORTALS_FEE, TONNEL_FEE, TRANSFER_FEE, MIN_PROFIT
from models import ArbitrageOpportunity
from database import db_session
import logging

logger = logging.getLogger(__name__)

def calculate_profit(auction_price, portals_price, tonnel_price):
    """Рассчитать прибыль для двух сценариев арбитража"""
    # Сценарий 1: Купить на аукционе → Продать на Portals
    sell_on_portals = portals_price * (1 - PORTALS_FEE) - auction_price - TRANSFER_FEE
    
    # Сценарий 2: Купить на аукционе → Продать на Tonnel
    sell_on_tonnel = tonnel_price * (1 - TONNEL_FEE) - auction_price - TRANSFER_FEE
    
    return max(sell_on_portals, sell_on_tonnel)

def find_arbitrage_opportunities(portals_data, tonnel_auctions):
    """Найти арбитражные возможности"""
    opportunities = []
    
    # Анализ аукционов Tonnel
    for auction in tonnel_auctions:
        try:
            # Поиск соответствующего подарка на Portals
            matching_gift = next(
                (g for g in portals_data if g['id'] == auction['gift_id']),
                None
            )
            
            if matching_gift:
                portals_price = float(matching_gift['price'])
                auction_price = float(auction['current_bid'])
                profit = calculate_profit(auction_price, portals_price, 0)
                
                if profit >= MIN_PROFIT:
                    opportunities.append({
                        "gift_name": auction['gift_name'],
                        "model": auction['model'],
                        "auction_price": auction_price,
                        "portals_price": portals_price,
                        "tonnel_price": 0,
                        "profit": profit,
                        "auction_end_time": auction['end_time'],
                        "marketplace": "Tonnel"
                    })
        except Exception as e:
            logger.error(f"Error processing auction {auction['id']}: {str(e)}")
    
    # Добавить логику для Portals аукционов
    # ...
    
    return opportunities

def save_opportunities(opportunities):
    """Сохранить возможности в БД"""
    try:
        # Очистить старые записи
        db_session.query(ArbitrageOpportunity).delete()
        
        # Добавить новые
        for opp in opportunities:
            db_session.add(ArbitrageOpportunity(**opp))
        
        db_session.commit()
        return len(opportunities)
    except Exception as e:
        db_session.rollback()
        logger.error(f"Database save error: {str(e)}")
        return 0
