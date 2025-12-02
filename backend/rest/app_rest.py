from flask import jsonify
import db.store_repo as repo 

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
        