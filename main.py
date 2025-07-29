# main.py

import telebot
from telebot import types
import sqlite3
import requests
import time
import os
from dotenv import load_dotenv
from utils import fetch_market_data, calculate_profit, update_tokens

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
DB_PATH = os.getenv('DB_PATH')

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Создание базы данных SQLite
def init_db():
    conn = sqlite3.connect(DB_PATH)
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

# Обновление данных о подарках
def update_gifts():
    # Получение данных с API маркетплейсов
    portals_data = fetch_market_data('portals')
    tonnel_data = fetch_market_data('tonnel')
    mrkt_data = fetch_market_data('mrkt')

    # Расчет прибыли
    for gift in portals_data:
        profit = calculate_profit(gift, portals_data, tonnel_data, mrkt_data)
        if profit > 0.1:  # Фильтр по минимальной прибыли
            save_to_db(gift, profit)

# Сохранение данных в БД
def save_to_db(gift, profit):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO gifts (name, model, portals_price, tonnel_price, mrkt_price, auction_end_time, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (gift['name'], gift['model'], gift['portals_price'], gift['tonnel_price'], gift['mrkt_price'], gift['auction_end_time'], profit))
    conn.commit()
    conn.close()

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Арбитраж"), types.KeyboardButton("Аукцион"))
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите раздел:", reply_markup=markup)

# Обработка выбора раздела
@bot.message_handler(func=lambda message: True)
def handle_choice(message):
    if message.text == "Арбитраж":
        arbitrage(message)
    elif message.text == "Аукцион":
        auction(message)

# Арбитраж
def arbitrage(message):
    # Получение данных из БД
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gifts ORDER BY profit DESC')
    gifts = cursor.fetchall()
    conn.close()

    response = "Список арбитражных возможностей:\n"
    for gift in gifts:
        response += f"🎁 {gift[1]} ({gift[2]})\n"
        response += f"💰 Portals: {gift[3]} TON | Tonnel: {gift[4]} TON | MRKT: {gift[5]} TON\n"
        response += f"📈 Прибыль: {gift[6]} TON\n\n"

    bot.send_message(message.chat.id, response)

# Аукцион
def auction(message):
    # Логика аукциона (можно расширить)
    bot.send_message(message.chat.id, "В разработке...")

# Автоматическое обновление данных каждые 30 секунд
def auto_update():
    while True:
        try:
            update_gifts()
            print("Обновление данных выполнено.")
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
        time.sleep(30)

if __name__ == "__main__":
    init_db()
    update_tokens()  # Обновление токенов API
    auto_update_thread = threading.Thread(target=auto_update)
    auto_update_thread.start()
    bot.polling(none_stop=True)
