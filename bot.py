import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен бота
BOT_TOKEN = "8404158706:AAEPZiiYaCeTKeYtxrFMxKGP6Cr2prKs09U"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Клавиатура
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛍 Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton("ℹ️ О магазине", callback_data="about")],
        [InlineKeyboardButton("📞 Поддержка", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
👋 Привет, {user.first_name}!

✅ Бот работает! Магазин открыт!

🛍 Используйте кнопки ниже для навигации.
"""
    await update.message.reply_text(welcome_text, reply_markup=main_menu())

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "catalog":
        await query.edit_message_text("🛍 Каталог товаров:\n\nТовары появятся скоро!", reply_markup=main_menu())
    elif query.data == "about":
        await query.edit_message_text("🏪 О нашем магазине\n\nТестовый Telegram магазин!", reply_markup=main_menu())
    elif query.data == "support":
        await query.edit_message_text("📞 Поддержка\n\nСвяжитесь с администратором.", reply_markup=main_menu())

def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем бота
    print("🛍 Бот-магазин запущен!")
    application.run_polling()

if __name__ == "__main__":
    main()
