from apscheduler.schedulers.background import BackgroundScheduler
from api.portals_api import fetch_portals_data
from api.tonnel_api import fetch_tonnel_data
from services.arbitrage import find_arbitrage_opportunities, save_opportunities
import logging
from config import UPDATE_INTERVAL

logger = logging.getLogger(__name__)

def update_data():
    """Основная функция обновления данных"""
    try:
        logger.info("Starting data update...")
        
        # Получить данные с маркетплейсов
        portals_data = fetch_portals_data()
        tonnel_auctions = fetch_tonnel_data()
        
        # Рассчитать арбитраж
        opportunities = find_arbitrage_opportunities(portals_data, tonnel_auctions)
        
        # Сохранить в БД
        count = save_opportunities(opportunities)
        logger.info(f"Update completed. Found {count} opportunities.")
        
    except Exception as e:
        logger.error(f"Update failed: {str(e)}")

def start_scheduler():
    """Запустить фоновое обновление"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        update_data,
        'interval',
        seconds=UPDATE_INTERVAL,
        next_run_time=datetime.now()  # Запустить сразу
    )
    scheduler.start()
    logger.info(f"Scheduler started with {UPDATE_INTERVAL} sec interval")
