# -*- coding: utf-8 -*-
"""
Schema de Base de Datos para Onsen Coffee - E-commerce de Café de Especialidad
"""

import sqlite3
import os

# Ruta de la base de datos en la carpeta db
DB_PATH = os.path.join(os.path.dirname(__file__), 'onsen-coffee.db')

def get_connection():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    """Crea las 6 tablas principales del e-commerce"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. USUARIOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            role VARCHAR(20) DEFAULT 'customer' CHECK(role IN ('customer', 'admin')),
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. PRODUCTOS (Cafés)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            origin VARCHAR(100),
            roast VARCHAR(50) CHECK(roast IN ('claro', 'medio', 'oscuro')),
            process VARCHAR(50),
            flavor_notes TEXT,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            weight_grams INTEGER DEFAULT 250,
            stock INTEGER DEFAULT 0,
            image_url TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. PEDIDOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status VARCHAR(30) DEFAULT 'pending' CHECK(status IN ('pending', 'paid', 'shipped', 'delivered', 'cancelled')),
            subtotal DECIMAL(10,2) NOT NULL,
            shipping_cost DECIMAL(10,2) DEFAULT 0,
            total DECIMAL(10,2) NOT NULL,
            shipping_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # 4. ITEMS DEL PEDIDO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Índices
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)')
    
    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente!")

def insert_seed_data():
    """Inserta datos de ejemplo"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Usuarios de ejemplo
    users = [
        ('admin@onsencoffee.com', 'hashed_admin123', 'Carlos', 'Mendoza', '5551234567', 'admin'),
        ('maria@example.com', 'hashed_pass123', 'María', 'García', '5559876543', 'customer'),
        ('juan@example.com', 'hashed_pass456', 'Juan', 'López', '5554567890', 'customer'),
        ('ana@example.com', 'hashed_pass789', 'Ana', 'Martínez', '5553216549', 'customer'),
        ('pedro@example.com', 'hashed_pass321', 'Pedro', 'Sánchez', '5557894561', 'customer')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO users (email, password_hash, first_name, last_name, phone, role)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', users)
    
    # Productos de ejemplo
    products = [
        ('Ethiopian Yirgacheffe', 'Etiopía', 'medio', 'Lavado', 'Floral, cítrico, bergamota', 'Café de especialidad con notas brillantes', 299.00, 250, 50, '/images/ethiopia.jpg'),
        ('Colombian Geisha', 'Colombia', 'claro', 'Honey', 'Jazmín, durazno, miel', 'Geisha excepcional de finca de altura', 450.00, 250, 30, '/images/geisha.jpg'),
        ('Kenyan AA', 'Kenia', 'medio', 'Lavado', 'Grosella, tomate, vino', 'Acidez vibrante y compleja', 320.00, 250, 40, '/images/kenya.jpg'),
        ('Sumatra Mandheling', 'Indonesia', 'oscuro', 'Wet-hulled', 'Chocolate, terroso, especias', 'Cuerpo intenso y notas profundas', 280.00, 250, 45, '/images/sumatra.jpg'),
        ('Costa Rica Tarrazú', 'Costa Rica', 'medio', 'Lavado', 'Manzana verde, caramelo, nuez', 'Balance perfecto y dulzura natural', 310.00, 250, 35, '/images/costarica.jpg'),
        ('Guatemala Antigua', 'Guatemala', 'medio', 'Lavado', 'Chocolate, nuez, cítrico', 'Cuerpo completo con final dulce', 285.00, 250, 60, '/images/guatemala.jpg'),
        ('Brazil Santos', 'Brasil', 'oscuro', 'Natural', 'Nuez, chocolate, bajo en acidez', 'Suave y equilibrado para espresso', 220.00, 250, 80, '/images/brazil.jpg'),
        ('Panama Geisha', 'Panamá', 'claro', 'Lavado', 'Jazmín, bergamota, tropical', 'El café más exclusivo del mundo', 890.00, 250, 15, '/images/panama.jpg')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO products (name, origin, roast, process, flavor_notes, description, price, weight_grams, stock, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products)
    
    # Pedidos de ejemplo
    orders = [
        (2, 'delivered', 599.00, 99.00, 698.00, 'Av. Reforma 123, CDMX, CP 06600'),
        (2, 'shipped', 450.00, 99.00, 549.00, 'Av. Reforma 123, CDMX, CP 06600'),
        (3, 'paid', 920.00, 0.00, 920.00, 'Calle Juárez 456, Guadalajara, CP 44100'),
        (4, 'pending', 285.00, 99.00, 384.00, 'Blvd. Independencia 789, Monterrey, CP 64000'),
        (5, 'delivered', 1780.00, 0.00, 1780.00, 'Calle 5 de Mayo 321, Puebla, CP 72000'),
        (3, 'cancelled', 320.00, 99.00, 419.00, 'Calle Juárez 456, Guadalajara, CP 44100')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO orders (user_id, status, subtotal, shipping_cost, total, shipping_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', orders)
    
    # Items de pedidos
    order_items = [
        (1, 1, 2, 299.00),  # Pedido 1: 2x Ethiopian
        (2, 2, 1, 450.00),  # Pedido 2: 1x Colombian Geisha
        (3, 3, 2, 320.00),  # Pedido 3: 2x Kenyan
        (3, 4, 1, 280.00),  # Pedido 3: 1x Sumatra
        (4, 6, 1, 285.00),  # Pedido 4: 1x Guatemala
        (5, 8, 2, 890.00),  # Pedido 5: 2x Panama Geisha
        (6, 3, 1, 320.00),  # Pedido 6: 1x Kenyan (cancelado)
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    ''', order_items)
    
    conn.commit()
    conn.close()
    print("✅ Datos de ejemplo insertados!")

if __name__ == '__main__':
    create_tables()
    insert_seed_data()

