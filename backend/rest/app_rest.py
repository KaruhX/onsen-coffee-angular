from flask import jsonify, session, request
import repository.store_repo as repo

def register_routes(app):
    rest_route = "/api"

    @app.route(f"{rest_route}/")
    def init_rest():
        return "Rest Services OK"

    @app.route(f"{rest_route}/coffees")
    def obtainCoffees():
        return jsonify(repo.obtainCoffees())

    @app.route(f"{rest_route}/users")
    def obtainUsers():
        return jsonify(repo.obtainUsers())

    @app.route(f"{rest_route}/coffees/<int:coffee_id>")
    def obtainCoffeeById(coffee_id):
        return jsonify(repo.obtainCoffeeById(coffee_id))

    @app.route(f"{rest_route}/cart", methods=["GET"])
    def getCart():
        cart = session.get('cart', [])
        if not isinstance(cart, list):
            cart = []
            session['cart'] = cart
        return jsonify(cart)

    @app.route(f"{rest_route}/cart", methods=["POST"])
    def addToCart():
        cart = session.get('cart', [])
        if not isinstance(cart, list):
            cart = []

        data = request.get_json()
        coffee_id = data.get("coffeeId")
        quantity = data.get("quantity", 1)

        found = False
        for item in cart:
            if item.get('coffeeId') == coffee_id:
                item['quantity'] += quantity
                found = True
                break
        
        if not found:
            cart.append({'coffeeId': coffee_id, 'quantity': quantity})

        session['cart'] = cart
        return jsonify({"status": "ok", "cart": cart})

    @app.route(f"{rest_route}/cart/<int:coffee_id>", methods=["PUT"])
    def updateCartItem(coffee_id):
        cart = session.get('cart', [])
        if not isinstance(cart, list):
            cart = []

        data = request.get_json()
        quantity = data.get("quantity", 1)

        for item in cart:
            if item.get('coffeeId') == coffee_id:
                item['quantity'] = quantity
                break

        session['cart'] = cart
        return jsonify({"status": "ok", "cart": cart})

    @app.route(f"{rest_route}/cart/<int:coffee_id>", methods=["DELETE"])
    def removeFromCart(coffee_id):
        cart = session.get('cart', [])
        if not isinstance(cart, list):
            cart = []
        cart = [item for item in cart if item.get('coffeeId') != coffee_id]
        session['cart'] = cart
        return jsonify({"status": "ok", "cart": cart})

    @app.route(f"{rest_route}/cart", methods=["DELETE"])
    def clearCart():
        session['cart'] = []
        return jsonify({"status": "ok", "cart": []})
    
    # ============ ORDERS ENDPOINTS ============
    
    @app.route(f"{rest_route}/orders", methods=["POST"])
    def createOrder():
        try:
            data = request.get_json()
            
            # Validar campos requeridos
            required_fields = ['customer_name', 'customer_email', 'shipping_address', 'items']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({"error": f"El campo {field} es requerido"}), 400
            
            if not data.get('items') or len(data.get('items', [])) == 0:
                return jsonify({"error": "El carrito está vacío"}), 400
            
            result = repo.registerOrder(data)
            
            # Limpiar carrito después de crear pedido
            session['cart'] = []
            
            return jsonify(result)
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": f"Error al procesar pedido: {str(e)}"}), 500
    
    @app.route(f"{rest_route}/orders/<int:order_id>")
    def getOrder(order_id):
        order = repo.getOrderById(order_id)
        if not order:
            return jsonify({"error": "Pedido no encontrado"}), 404
        return jsonify(order)
    
    @app.route(f"{rest_route}/orders/by-email/<email>")
    def getOrdersByEmail(email):
        orders = repo.getOrdersByEmail(email)
        return jsonify(orders)
    
    @app.route(f"{rest_route}/orders")
    def getAllOrders():
        orders = repo.getAllOrders()
        return jsonify(orders)
    
    @app.route(f"{rest_route}/orders/<int:order_id>/status", methods=["PUT"])
    def updateOrderStatus(order_id):
        data = request.get_json()
        status = data.get('status')
        tracking_number = data.get('tracking_number')
        
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
        if status not in valid_statuses:
            return jsonify({"error": f"Estado no válido. Usa: {', '.join(valid_statuses)}"}), 400
        
        result = repo.updateOrderStatus(order_id, status, tracking_number)
        return jsonify(result)