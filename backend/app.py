import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import init_db, db_session
from models import ArbitrageOpportunity
from services.scheduler import start_scheduler
from config import BOT_TOKEN, ADMIN_CHAT_ID

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Разрешить CORS для фронтенда
init_db()  # Инициализация БД

@app.route('/api/opportunities', methods=['GET'])
def get_opportunities():
    """Получить арбитражные возможности с фильтрацией"""
    try:
        min_profit = float(request.args.get('min_profit', 0.1))
        max_price = float(request.args.get('max_price', 1000))
        sort_by = request.args.get('sort_by', 'profit_desc')
        
        query = db_session.query(ArbitrageOpportunity).filter(
            ArbitrageOpportunity.profit >= min_profit,
            ArbitrageOpportunity.auction_price <= max_price
        )
        
        # Сортировка
        if sort_by == 'profit_desc':
            query = query.order_by(ArbitrageOpportunity.profit.desc())
        elif sort_by == 'end_time_asc':
            query = query.order_by(ArbitrageOpportunity.auction_end_time.asc())
        
        opportunities = [opp.to_dict() for opp in query.all()]
        return jsonify({"success": True, "data": opportunities})
    
    except Exception as e:
        logger.error(f"Error fetching opportunities: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/update', methods=['POST'])
def manual_update():
    """Ручной запуск обновления данных"""
    try:
        # В реальной реализации здесь вызов логики обновления
        logger.info("Manual update triggered")
        return jsonify({"success": True, "message": "Update initiated"})
    except Exception as e:
        logger.error(f"Manual update failed: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    start_scheduler()  # Запуск фонового обновления
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
