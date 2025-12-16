from db.connection_supabase import get_supabase_client

def get_client():
    """Obtiene el cliente de Supabase con permisos de service_role"""
    return get_supabase_client(use_service_key=True)

def obtainCoffees():
    client = get_client()
    response = client.table('products').select('*').eq('is_active', True).execute()
    return response.data

def obtainCoffeeById(coffee_id):
    client = get_client()
    response = client.table('products').select('*').eq('id', coffee_id).eq('is_active', True).execute()
    return response.data[0] if response.data else {"error": "Coffee not found"}

def saveNewCoffee(coffee_data):
    """Guarda un nuevo producto con todos los campos"""
    client = get_client()
    
    # Generar slug si no existe
    slug = coffee_data.get('slug')
    if not slug:
        name = coffee_data.get('name', '')
        slug = name.lower().replace(' ', '-').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    
    data = {
        'name': coffee_data.get('name'),
        'slug': slug,
        'description': coffee_data.get('description', ''),
        'short_description': coffee_data.get('short_description'),
        'origin': coffee_data.get('origin'),
        'roast': coffee_data.get('roast', 'medio'),
        'process': coffee_data.get('process'),
        'altitude': coffee_data.get('altitude'),
        'flavor_notes': coffee_data.get('flavor_notes'),
        'price': coffee_data.get('price'),
        'old_price': coffee_data.get('old_price'),
        'weight_grams': coffee_data.get('weight_grams', 250),
        'stock': coffee_data.get('stock', 0),
        'category': coffee_data.get('category', 'coffee'),
        'image_url': coffee_data.get('image_url'),
        'featured': coffee_data.get('featured', False),
        'is_new': coffee_data.get('is_new', False),
        'is_active': True
    }
    
    response = client.table('products').insert(data).execute()
    return {"status": "ok", "id": response.data[0]['id']}

def obtainUsers():
    client = get_client()
    response = client.table('users').select('id, email, first_name, last_name, phone, role, is_active, created_at').execute()
    return response.data

def obtainUserById(user_id):
    client = get_client()
    response = client.table('users').select('id, email, first_name, last_name, phone, role, is_active, created_at').eq('id', user_id).execute()
    return response.data[0] if response.data else {"error": "User not found"}
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
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
        order_id = cur.fetchone()['id']

        for item in items:
            product_id = int(item.get('product_id'))
            quantity = int(item.get('quantity', 1))
            price = float(item.get('price', 0))
            
            # Verificar que el producto existe
            cur.execute("SELECT id FROM products WHERE id = %s", (product_id,))
            verify = cur.fetchone()
            if not verify:
                raise ValueError(f"Producto con ID {product_id} no encontrado")
            
            cur.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price)
                VALUES (%s, %s, %s, %s)
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
    cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
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
        WHERE oi.order_id = %s
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
        WHERE customer_email = %s 
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
            SET status = %s, tracking_number = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (status, tracking_number, order_id))
    else:
        cur.execute("""
            UPDATE orders 
            SET status = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s
        """, (status, order_id))
    con.commit()
    con.close()
    return {"status": "ok"}

def updateOrderInfo(order_id, data):
    """Actualiza información del pedido (dirección, teléfono, notas)"""
    con = get_connection()
    cur = con.cursor()
    
    # Campos permitidos para actualizar
    allowed_fields = {
        'customer_phone': 'customer_phone',
        'shipping_address': 'shipping_address',
        'shipping_city': 'shipping_city',
        'shipping_postal_code': 'shipping_postal_code',
        'shipping_country': 'shipping_country',
        'notes': 'notes'
    }
    
    updates = []
    values = []
    
    for field, column in allowed_fields.items():
        if field in data:
            updates.append(f"{column} = %s")
            values.append(data[field])
    
    if not updates:
        con.close()
        return {"error": "No hay campos para actualizar"}
    
    # Añadir updated_at
    updates.append("updated_at = CURRENT_TIMESTAMP")
    values.append(order_id)
    
    query = f"UPDATE orders SET {', '.join(updates)} WHERE id = %s"
    cur.execute(query, values)
    con.commit()
    
    # Retornar el pedido actualizado
    cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    row = cur.fetchone()
    order = dict(row) if row else None
    con.close()
    
    return order

def obtainOrders(status_filter='all'):
    con = get_connection()
    cur = con.cursor()
    
    if status_filter == 'all':
        cur.execute("""
            SELECT * FROM orders 
            ORDER BY created_at DESC
        """)
    else:
        cur.execute("""
            SELECT * FROM orders 
            WHERE status = %s
            ORDER BY created_at DESC
        """, (status_filter,))
    
    orders = []
    for row in cur.fetchall():
        order = dict(row)
        
        # Obtener items del pedido
        cur_items = con.cursor()
        cur_items.execute("""
            SELECT oi.*, p.name, p.image_url
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = %s
        """, (order['id'],))
        
        items = []
        for item_row in cur_items.fetchall():
            item_dict = dict(item_row)
            items.append({
                'name': item_dict['name'],
                'quantity': item_dict['quantity'],
                'price': item_dict['unit_price'],
                'image_url': item_dict.get('image_url')
            })
        
        order['items'] = items
        orders.append(order)
    
    con.close()
    return orders

def deleteOrder(order_id):
    con = get_connection()
    cur = con.cursor()
    # Primero eliminar los items del pedido
    cur.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
    # Luego eliminar el pedido
    cur.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    con.commit()
    con.close()
    return {"status": "ok"}

def updateUserRole(user_id, role):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
    con.commit()
    con.close()
    return {"status": "ok"}

def deleteUser(user_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE users SET is_active = FALSE WHERE id = %s", (user_id,))
    con.commit()
    con.close()
    return {"status": "ok"}

def updateCoffee(coffee_data):
    """Actualiza un producto con todos los campos disponibles"""
    con = get_connection()
    cur = con.cursor()
    coffee_id = coffee_data.get('id')
    
    cur.execute("""
        UPDATE products 
        SET name = %s, slug = %s, description = %s, short_description = %s, 
            origin = %s, roast = %s, process = %s, altitude = %s,
            flavor_notes = %s, price = %s, old_price = %s, weight_grams = %s,
            stock = %s, category = %s, image_url = %s, featured = %s, is_new = %s
        WHERE id = %s
    """, (
        coffee_data.get('name'),
        coffee_data.get('slug'),
        coffee_data.get('description'),
        coffee_data.get('short_description'),
        coffee_data.get('origin'),
        coffee_data.get('roast'),
        coffee_data.get('process'),
        coffee_data.get('altitude'),
        coffee_data.get('flavor_notes'),
        coffee_data.get('price'),
        coffee_data.get('old_price'),
        coffee_data.get('weight_grams', 250),
        coffee_data.get('stock'),
        coffee_data.get('category', 'coffee'),
        coffee_data.get('image_url'),
        coffee_data.get('featured', False),
        coffee_data.get('is_new', False),
        coffee_id
    ))
    con.commit()
    con.close()
    return {"status": "ok"}

def deleteCoffee(coffee_id):
    con = get_connection()
    cur = con.cursor()
    cur.execute("UPDATE products SET is_active = FALSE WHERE id = %s", (coffee_id,))
    con.commit()
    con.close()
    return {"status": "ok"}

def createUser(user_data):
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO users (email, first_name, last_name, phone, role, is_active)
        VALUES (%s, %s, %s, %s, %s, TRUE)
        RETURNING id
    """, (
        user_data.get('email'),
        user_data.get('first_name'),
        user_data.get('last_name'),
        user_data.get('phone', ''),
        user_data.get('role', 'user')
    ))
    user_id = cur.fetchone()['id']
    con.commit()
    con.close()
    return {"status": "ok", "id": user_id}

# ============================================
# MENSAJES DE CONTACTO
# ============================================

def createContactMessage(data):
    """Crea un nuevo mensaje de contacto"""
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO contact_messages (name, email, subject, message, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, created_at
    """, (
        data.get('name'),
        data.get('email'),
        data.get('subject'),
        data.get('message'),
        data.get('status', 'new')
    ))
    result = cur.fetchone()
    con.commit()
    con.close()
    return {"status": "ok", "id": result['id'], "created_at": result['created_at']}

def getAllContactMessages(status_filter=None):
    """Obtiene todos los mensajes de contacto, opcionalmente filtrados por estado"""
    con = get_connection()
    cur = con.cursor()
    
    if status_filter:
        cur.execute("""
            SELECT * FROM contact_messages 
            WHERE status = %s 
            ORDER BY created_at DESC
        """, (status_filter,))
    else:
        cur.execute("SELECT * FROM contact_messages ORDER BY created_at DESC")
    
    messages = [dict(row) for row in cur.fetchall()]
    con.close()
    return messages

def getContactMessageById(message_id):
    """Obtiene un mensaje de contacto por ID"""
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM contact_messages WHERE id = %s", (message_id,))
    row = cur.fetchone()
    message = dict(row) if row else None
    con.close()
    return message

def updateContactMessageStatus(message_id, status):
    """Actualiza el estado de un mensaje de contacto"""
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        UPDATE contact_messages 
        SET status = %s 
        WHERE id = %s
        RETURNING *
    """, (status, message_id))
    row = cur.fetchone()
    result = dict(row) if row else None
    con.commit()
    con.close()
    return result

def deleteContactMessage(message_id):
    """Elimina un mensaje de contacto"""
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM contact_messages WHERE id = %s", (message_id,))
    con.commit()
    con.close()
    return {"status": "ok"}

# ============================================
# REVIEWS DE PRODUCTOS
# ============================================

def createProductReview(data):
    """Crea una nueva review de producto"""
    con = get_connection()
    cur = con.cursor()
    
    # Validar rating
    rating = int(data.get('rating', 5))
    if rating < 1 or rating > 5:
        return {"error": "Rating debe estar entre 1 y 5"}
    
    cur.execute("""
        INSERT INTO product_reviews (product_id, user_id, name, rating, comment)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, created_at
    """, (
        data.get('product_id'),
        data.get('user_id'),
        data.get('name'),
        rating,
        data.get('comment')
    ))
    result = cur.fetchone()
    
    # Actualizar rating promedio del producto
    cur.execute("""
        UPDATE products 
        SET rating = (
            SELECT AVG(rating)::DECIMAL(3,2) 
            FROM product_reviews 
            WHERE product_id = %s
        ),
        reviews_count = (
            SELECT COUNT(*) 
            FROM product_reviews 
            WHERE product_id = %s
        )
        WHERE id = %s
    """, (data.get('product_id'), data.get('product_id'), data.get('product_id')))
    
    con.commit()
    con.close()
    return {"status": "ok", "id": result['id'], "created_at": result['created_at']}

def getProductReviews(product_id):
    """Obtiene todas las reviews de un producto"""
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT * FROM product_reviews 
        WHERE product_id = %s 
        ORDER BY created_at DESC
    """, (product_id,))
    reviews = [dict(row) for row in cur.fetchall()]
    con.close()
    return reviews

def deleteProductReview(review_id):
    """Elimina una review y actualiza el rating del producto"""
    con = get_connection()
    cur = con.cursor()
    
    # Obtener product_id antes de eliminar
    cur.execute("SELECT product_id FROM product_reviews WHERE id = %s", (review_id,))
    row = cur.fetchone()
    if not row:
        con.close()
        return {"error": "Review no encontrada"}
    
    product_id = row['product_id']
    
    # Eliminar review
    cur.execute("DELETE FROM product_reviews WHERE id = %s", (review_id,))
    
    # Actualizar rating del producto
    cur.execute("""
        UPDATE products 
        SET rating = COALESCE((
            SELECT AVG(rating)::DECIMAL(3,2) 
            FROM product_reviews 
            WHERE product_id = %s
        ), 0),
        reviews_count = (
            SELECT COUNT(*) 
            FROM product_reviews 
            WHERE product_id = %s
        )
        WHERE id = %s
    """, (product_id, product_id, product_id))
    
    con.commit()
    con.close()
    return {"status": "ok"}

# ============================================
# BÚSQUEDA Y FILTRADO AVANZADO
# ============================================

def searchProducts(query=None, category=None, roast=None, min_price=None, max_price=None, featured=None, is_new=None):
    """Búsqueda avanzada de productos con múltiples filtros"""
    con = get_connection()
    cur = con.cursor()
    
    conditions = ["is_active = TRUE"]
    params = []
    
    if query:
        conditions.append("(name ILIKE %s OR description ILIKE %s OR origin ILIKE %s)")
        search_term = f"%{query}%"
        params.extend([search_term, search_term, search_term])
    
    if category:
        conditions.append("category = %s")
        params.append(category)
    
    if roast:
        conditions.append("roast = %s")
        params.append(roast)
    
    if min_price is not None:
        conditions.append("price >= %s")
        params.append(min_price)
    
    if max_price is not None:
        conditions.append("price <= %s")
        params.append(max_price)
    
    if featured is not None:
        conditions.append("featured = %s")
        params.append(featured)
    
    if is_new is not None:
        conditions.append("is_new = %s")
        params.append(is_new)
    
    where_clause = " AND ".join(conditions)
    query_sql = f"SELECT * FROM products WHERE {where_clause} ORDER BY created_at DESC"
    
    cur.execute(query_sql, params)
    products = [dict(row) for row in cur.fetchall()]
    con.close()
    return products

def getProductBySlug(slug):
    """Obtiene un producto por su slug"""
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE slug = %s AND is_active = TRUE", (slug,))
    row = cur.fetchone()
    product = dict(row) if row else None
    con.close()
    return product

