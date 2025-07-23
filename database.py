import sqlite3
import logging
from config import Config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name=Config.DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            # Таблица для токенов API
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS api_tokens (
                    service TEXT PRIMARY KEY,
                    access_token TEXT NOT NULL,
                    refresh_token TEXT NOT NULL,
                    expires_at TIMESTAMP
                )
            ''')
            
            # Таблица для истории арбитража
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS arbitrage_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nft_id TEXT NOT NULL,
                    profit REAL NOT NULL,
                    action_type TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица для пользовательских настроек
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    chat_id INTEGER PRIMARY KEY,
                    min_profit REAL DEFAULT 0.1,
                    update_interval INTEGER DEFAULT 45
                )
            ''')
            self.conn.commit()
        except Exception as e:
            logger.error(f"Database error: {e}")
    
    def save_token(self, service: str, access_token: str, refresh_token: str, expires_at: float):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO api_tokens 
                (service, access_token, refresh_token, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (service, access_token, refresh_token, expires_at))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Token save error: {e}")
    
    def get_token(self, service: str) -> tuple:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT access_token, refresh_token, expires_at 
                FROM api_tokens WHERE service = ?
            ''', (service,))
            return cursor.fetchone()
        except Exception as e:
            logger.error(f"Token retrieval error: {e}")
            return None
    
    def save_arbitrage_result(self, result: 'ArbitrageResult'):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO arbitrage_history 
                (nft_id, profit, action_type)
                VALUES (?, ?, ?)
            ''', (result.item.id, result.profit, result.action))
            self.conn.commit()
        except Exception as e:
            logger.error(f"History save error: {e}")
    
    # Другие методы для работы с настройками...

db = Database()
