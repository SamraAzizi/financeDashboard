import sqlite3
from datetime import datetime

def initialize_database():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            type TEXT NOT NULL
        )
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL
        )
    ''')
    
    # Insert default categories if they don't exist
    default_categories = [
        ('Salary', 'income'),
        ('Investments', 'income'),
        ('Food', 'expense'),
        ('Transport', 'expense'),
        ('Utilities', 'expense'),
        ('Entertainment', 'expense'),
        ('Shopping', 'expense'),
        ('Healthcare', 'expense'),
        ('Education', 'expense')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO categories (name, type)
        VALUES (?, ?)
    ''', default_categories)
    
    conn.commit()
    conn.close()

def add_transaction(date, category, amount, description, type):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO transactions (date, category, amount, description, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, category, amount, description, type))
    
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
    transactions = cursor.fetchall()
    
    conn.close()
    return transactions

def get_categories():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, type FROM categories')
    categories = cursor.fetchall()
    
    conn.close()
    return categories 