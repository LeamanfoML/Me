from config import Config
from models import NFTItem, ArbitrageResult
from datetime import datetime

class ArbitrageCalculator:
    def __init__(self):
        self.min_profit = Config.MIN_PROFIT
        self.transfer_fee = Config.TRANSFER_FEE
        self.portals_fee = Config.PORTALS_FEE
        self.tonnel_fee = Config.TONNEL_FEE
    
    def calculate_profit(self, item: NFTItem) -> ArbitrageResult:
        # Арбитраж: аукцион Portals -> рынок Tonnel
        portals_to_tonnel = self._calc_portals_to_tonnel(item)
        
        # Арбитраж: аукцион Tonnel -> рынок Portals
        tonnel_to_portals = self._calc_tonnel_to_portals(item)
        
        # Выбираем наиболее выгодный вариант
        if portals_to_tonnel.profit > tonnel_to_portals.profit:
            return portals_to_tonnel
        return tonnel_to_portals
    
    def _calc_portals_to_tonnel(self, item: NFTItem) -> ArbitrageResult:
        """
        Расчет: Купить на аукционе Portals → Продать на рынке Tonnel
        """
        # Затраты = текущая ставка + комиссия перевода
        costs = item.current_bid + self.transfer_fee
        
        # Доход = цена на Tonnel минус комиссия Tonnel
        revenue = item.tonnel_price * (1 - self.tonnel_fee)
        
        profit = revenue - costs
        return ArbitrageResult(
            item=item,
            profit=round(profit, 2),
            action="auction_to_market"
        )
    
    def _calc_tonnel_to_portals(self, item: NFTItem) -> ArbitrageResult:
        """
        Расчет: Купить на аукционе Tonnel → Продать на рынке Portals
        """
        # Затраты = текущая ставка + комиссия перевода
        costs = item.current_bid + self.transfer_fee
        
        # Доход = цена на Portals минус комиссия Portals
        revenue = item.portals_price * (1 - self.portals_fee)
        
        profit = revenue - costs
        return ArbitrageResult(
            item=item,
            profit=round(profit, 2),
            action="market_to_auction"
        )
    
    def filter_opportunities(self, items: list[ArbitrageResult]) -> list[ArbitrageResult]:
        return [
            item for item in items 
            if item.profit >= self.min_profit
        ]
    
    def sort_by_profit(self, items: list[ArbitrageResult]) -> list[ArbitrageResult]:
        return sorted(items, key=lambda x: x.profit, reverse=True)
    
    def sort_by_end_time(self, items: list[ArbitrageResult]) -> list[ArbitrageResult]:
        return sorted(items, key=lambda x: x.item.end_time)
