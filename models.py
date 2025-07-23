from dataclasses import dataclass
from datetime import datetime

@dataclass
class NFTItem:
    id: str
    name: str
    model: str
    current_bid: float  # Текущая ставка в TON
    end_time: datetime  # Время окончания аукциона
    image_url: str
    
    # Цены на маркетплейсах
    portals_price: float = 0.0
    tonnel_price: float = 0.0
    calculated_profit: float = 0.0  # Расчетная прибыль

@dataclass
class ArbitrageResult:
    item: NFTItem
    profit: float
    action: str  # "auction_to_market" или "market_to_auction"
