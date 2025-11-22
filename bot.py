import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from database import db
from keyboards import *

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv('8404158706:AAEPZiiYaCeTKeYtxrFMxKGP6Cr2prKs09U')
ADMIN_ID = int(os.getenv('ADMIN_ID', '6539897544'))

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Корзины пользователей (в памяти)
user_carts = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в наш магазин! Здесь вы можете приобрести различные товары.

📱 Используйте кнопки ниже для навигации:
"""
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "main_menu":
        await query.edit_message_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )
    
    elif data == "catalog":
        products = db.get_products()
        if not products:
            await query.edit_message_text(
                "😔 В настоящий момент товаров нет в наличии.",
                reply_markup=main_menu()
            )
            return
        
        text = "🛍 Каталог товаров:\n\n"
        for product in products:
            text += f"▪️ {product[1]} - {product[3]}₽\n"
        
        await query.edit_message_text(
            text,
            reply_markup=catalog_keyboard(products)
        )
    
    elif data.startswith("product_"):
        product_id = data.split("_")[1]
        product = db.get_product(product_id)
        
        if product:
            text = f"""
📦 {product[1]}

💰 Цена: {product[3]}₽
📝 Описание: {product[2]}
🎯 Категория: {product[5] or 'Не указана'}
📦 В наличии: {product[6]} шт.
"""
            await query.edit_message_text(
                text,
                reply_markup=product_keyboard(product_id)
            )
    
    elif data.startswith("add_"):
        product_id = data.split("_")[1]
        product = db.get_product(product_id)
        
        if user_id not in user_carts:
            user_carts[user_id] = []
        
        user_carts[user_id].append({
            'id': product[0],
            'name': product[1],
            'price': product[3]
        })
        
        total = sum(item['price'] for item in user_carts[user_id])
        
        await query.edit_message_text(
            f"✅ Товар добавлен в корзину!\n\n"
            f"🛒 В вашей корзине: {len(user_carts[user_id])} товаров\n"
            f"💰 Общая сумма: {total}₽",
            reply_markup=buy_keyboard()
        )
    
    elif data == "checkout":
        if user_id not in user_carts or not user_carts[user_id]:
            await query.edit_message_text(
                "🛒 Ваша корзина пуста!",
                reply_markup=main_menu()
            )
            return
        
        cart = user_carts[user_id]
        total = sum(item['price'] for item in cart)
        
        order_id = db.create_order(
            user_id=user_id,
            user_name=query.from_user.full_name,
            products=cart,
            total_price=total
        )
        
        order_text = f"""
✅ Заказ #{order_id} оформлен!

📦 Состав заказа:
"""
        for item in cart:
            order_text += f"▪️ {item['name']} - {item['price']}₽\n"
        
        order_text += f"\n💰 Итого: {total}₽"
        order_text += f"\n\n📞 Для оплаты свяжитесь с администратором"
        
        user_carts[user_id] = []
        
        await query.edit_message_text(
            order_text,
            reply_markup=main_menu()
        )
        
        admin_text = f"""
🆕 Новый заказ #{order_id}

👤 Клиент: {query.from_user.full_name} (@{query.from_user.username})
💰 Сумма: {total}₽
"""
        await context.bot.send_message(ADMIN_ID, admin_text)
    
    elif data == "support":
        await query.edit_message_text(
            "📞 Свяжитесь с нами:\n\n"
            "👤 Администратор: @ваш_логин\n"
            "📧 Email: ваш@email.com",
            reply_markup=main_menu()
        )
    
    elif data == "about":
        await query.edit_message_text(
            "🏪 О нашем магазине\n\n"
            "Мы предлагаем качественные товары по доступным ценам!\n\n"
            "✅ Быстрая доставка\n"
            "✅ Качественный товар\n"
            "✅ Поддержка 24/7",
            reply_markup=main_menu()
        )

async def add_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав для этой команды")
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "Использование: /add_product 'Название' 'Описание' Цена [Категория] [Количество]"
        )
        return
    
    try:
        name = context.args[0]
        description = context.args[1]
        price = float(context.args[2])
        category = context.args[3] if len(context.args) > 3 else ""
        stock = int(context.args[4]) if len(context.args) > 4 else 1
        
        product_id = db.add_product(name, description, price, "", category, stock)
        
        await update.message.reply_text(f"✅ Товар '{name}' добавлен с ID {product_id}")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_product", add_product))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.run_polling()

if __name__ == "__main__":
    main()
