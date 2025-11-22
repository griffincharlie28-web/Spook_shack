import sqlite3
import json

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image TEXT,
                category TEXT,
                stock INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                products TEXT,
                total_price REAL,
                status TEXT DEFAULT 'новый',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def add_product(self, name, description, price, image="", category="", stock=1):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, description, price, image, category, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, price, image, category, stock))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_products(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE stock > 0')
        return cursor.fetchall()
    
    def get_product(self, product_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        return cursor.fetchone()
    
    def create_order(self, user_id, user_name, products, total_price):
        cursor = self.conn.cursor()
        products_json = json.dumps(products)
        cursor.execute('''
            INSERT INTO orders (user_id, user_name, products, total_price)
            VALUES (?, ?, ?, ?)
        ''', (user_id, user_name, products_json, total_price))
        self.conn.commit()
        return cursor.lastrowid

db = Database()
