from db.connection import get_connection

def obtainCoffees():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE is_active = 1")
    rows = cur.fetchall()
    coffees = [dict(row) for row in rows]
    con.close()
    return coffees

def obtainCoffeeById(coffee_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE id = ? AND is_active = 1", (coffee_id,))
    row = cur.fetchone()
    coffee = dict(row) if row else {"error": "Coffee not found"}
    con.close()
    return coffee

def saveNewCoffee(coffee_data):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO products (name, description, price, origin, is_active)
        VALUES (?, ?, ?, ?, 1)
    """, (
        coffee_data.get('name'),
        coffee_data.get('description'),
        coffee_data.get('price'),
        coffee_data.get('origin')
    ))
    con.commit()
    con.close()

def obtainUsers():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, email, first_name, last_name, phone, role, is_active, created_at FROM users")
    rows = cur.fetchall()
    users = [dict(row) for row in rows]
    con.close()
    return users

def obtainUserById(user_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, email, first_name, last_name, phone, role, is_active, created_at FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    user = dict(row) if row else {"error": "User not found"}
    con.close()
    return user
def registerOrder(order_data):
    con = get_connection()
    cur = con.cursor()
    
    # Validar campos requeridos
    if not order_data.get('items') or len(order_data.get('items', [])) == 0:
        raise ValueError("El pedido debe contener al menos un producto")
    
    # Calcular subtotal desde los items
    items = order_data.get('items', [])
    subtotal = 0
    for item in items:
        price = float(item.get('price', 0))
        quantity = int(item.get('quantity', 1))
        subtotal += price * quantity
    
    shipping_cost = float(order_data.get('shipping_cost', 4.99))
    total = subtotal + shipping_cost
    
    try:
        cur.execute("""
            INSERT INTO orders (
                user_id, status, subtotal, shipping_cost, total,
                customer_name, customer_email, customer_phone,
                shipping_address, shipping_city, shipping_postal_code, shipping_country,
                payment_method, payment_status, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data.get('user_id'),
            'pending',
            subtotal,
            shipping_cost,
            total,
            order_data.get('customer_name'),
            order_data.get('customer_email'),
            order_data.get('customer_phone'),
            order_data.get('shipping_address'),
            order_data.get('shipping_city'),
            order_data.get('shipping_postal_code'),
            order_data.get('shipping_country', 'España'),
            order_data.get('payment_method', 'card'),
            'pending',
            order_data.get('notes')
        ))
        order_id = cur.lastrowid

        for item in items:
            product_id = int(item.get('product_id'))
            quantity = int(item.get('quantity', 1))
            price = float(item.get('price', 0))
            
            # Verificar que el producto existe
            verify = cur.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
            if not verify:
                raise ValueError(f"Producto con ID {product_id} no encontrado")
            
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            """, (order_id, product_id, quantity, price))

        con.commit()
        con.close()
        return {"status": "ok", "order_id": order_id, "total": total}
    except Exception as e:
        con.rollback()
        con.close()
        raise e

def getOrderById(order_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()
    if not row:
        con.close()
        return None
    
    order = dict(row)
    
    # Obtener items del pedido
    cur.execute("""
        SELECT oi.*, p.name, p.image_url, p.origin 
        FROM order_items oi 
        JOIN products p ON oi.product_id = p.id 
        WHERE oi.order_id = ?
    """, (order_id,))
    items = [dict(item) for item in cur.fetchall()]
    order['items'] = items
    
    con.close()
    return order

def getOrdersByEmail(email):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT * FROM orders 
        WHERE customer_email = ? 
        ORDER BY created_at DESC
    """, (email,))
    orders = [dict(row) for row in cur.fetchall()]
    con.close()
    return orders

def getAllOrders():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = [dict(row) for row in cur.fetchall()]
    con.close()
    return orders

def updateOrderStatus(order_id, status, tracking_number=None):
    con = get_connection()
    cur = con.cursor()
    if tracking_number:
        cur.execute("""
            UPDATE orders 
            SET status = ?, tracking_number = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (status, tracking_number, order_id))
    else:
        cur.execute("""
            UPDATE orders 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (status, order_id))
    con.commit()
    con.close()
    return {"status": "ok"}