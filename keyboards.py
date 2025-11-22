from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("🛍 Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton("📦 Мои заказы", callback_data="my_orders")],
        [InlineKeyboardButton("ℹ️ О магазине", callback_data="about")],
        [InlineKeyboardButton("📞 Поддержка", callback_data="support")]
    ]
    return InlineKeyboardMarkup(keyboard)

def catalog_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                f"{product[1]} - {product[3]}₽", 
                callback_data=f"product_{product[0]}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def product_keyboard(product_id):
    keyboard = [
        [InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_{product_id}")],
        [InlineKeyboardButton("🔙 Назад к каталогу", callback_data="catalog")]
    ]
    return InlineKeyboardMarkup(keyboard)

def buy_keyboard():
    keyboard = [
        [InlineKeyboardButton("💳 Оплатить заказ", callback_data="checkout")],
        [InlineKeyboardButton("🔙 Продолжить покупки", callback_data="catalog")]
    ]
    return InlineKeyboardMarkup(keyboard)
