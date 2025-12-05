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