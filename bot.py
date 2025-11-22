import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Токен бота
BOT_TOKEN = "8404158706:AAEPZiiYaCeTKeYtxrFMxKGP6Cr2prKs09U"
ADMIN_ID = 6539897544

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Корзины пользователей
user_carts = {}

# Клавиатуры
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛍 Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton("ℹ️ О магазине", callback_data="about")],
        [InlineKeyboardButton("📞 Поддержка", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Команда /start
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в наш магазин!
Магазин работает в тестовом режиме.

📱 Используйте кнопки ниже:
"""
    update.message.reply_text(welcome_text, reply_markup=main_menu())

# Обработчик кнопок
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "catalog":
        query.edit_message_text("🛍 Каталог товаров:\n\nПока пусто! Добавьте товары через админку.", reply_markup=main_menu())
    elif query.data == "about":
        query.edit_message_text("🏪 О нашем магазине\n\nТестовый магазин в Telegram!", reply_markup=main_menu())
    elif query.data == "support":
        query.edit_message_text("📞 Поддержка\n\nС
