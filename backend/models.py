from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class ArbitrageOpportunity(Base):
    __tablename__ = 'arbitrage_opportunities'
    
    id = Column(Integer, primary_key=True)
    gift_name = Column(String(200), nullable=False)
    model = Column(String(50), nullable=False)
    auction_price = Column(Float, nullable=False)     # Текущая ставка на аукционе
    portals_price = Column(Float, nullable=False)     # Цена на Portals
    tonnel_price = Column(Float, nullable=False)      # Цена на Tonnel
    profit = Column(Float, nullable=False)            # Расчетная прибыль
    auction_end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    marketplace = Column(String(20), nullable=False)  # Источник аукциона
    
    def to_dict(self):
        return {
            "id": self.id,
            "gift_name": self.gift_name,
            "model": self.model,
            "auction_price": round(self.auction_price, 2),
            "portals_price": round(self.portals_price, 2),
            "tonnel_price": round(self.tonnel_price, 2),
            "profit": round(self.profit, 2),
            "auction_end_time": self.auction_end_time.isoformat(),
            "marketplace": self.marketplace
        }
