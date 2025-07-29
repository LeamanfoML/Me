# db.py

import sqlite3
import os

DB_PATH = os.getenv('DB_PATH')

# Соединение с базой данных
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# Создание таблицы
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            model TEXT,
            portals_price REAL,
            tonnel_price REAL,
            mrkt_price REAL,
            auction_end_time TEXT,
            profit REAL
        )
    ''')
    conn.commit()
    conn.close()

# Сохранение данных в БД
def save_to_db(name, model, portals_price, tonnel_price, mrkt_price, auction_end_time, profit):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO gifts (name, model, portals_price, tonnel_price, mrkt_price, auction_end_time, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, model, portals_price, tonnel_price, mrkt_price, auction_end_time, profit))
    conn.commit()
    conn.close()

# Получение данных из БД
def get_all_gifts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gifts ORDER BY profit DESC')
    gifts = cursor.fetchall()
    conn.close()
    return gifts
