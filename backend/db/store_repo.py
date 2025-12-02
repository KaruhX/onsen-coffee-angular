# -*- coding: utf-8 -*-
from flask import jsonify

def obtainCoffees():
    # Cafés de Prueba
    coffees = [
        {"id": 1, "name": "Ethiopian Yirgacheffe", "origin": "Etiopía", "roast": "Medio", "price": 14.99},
        {"id": 2, "name": "Colombian Geisha", "origin": "Panamá", "roast": "Claro", "price": 18.50},
        {"id": 3, "name": "Kenyan AA", "origin": "Kenia", "roast": "Medio", "price": 13.75},
        {"id": 4, "name": "Indonesian Sumatra Mandheling", "origin": "Indonesia", "roast": "Oscuro", "price": 12.99},
        {"id": 5, "name": "Costa Rican Tarrazú", "origin": "Costa Rica", "roast": "Medio", "price": 15.50}
    ]
    return coffees

def obtainUsers():
    # Usuarios de Prueba
    users = [
        {"id": 1, "username": "Chivo Valencia", "email": "chivo@example.com", "password": "12345"},
        {"id": 2, "username": "William Pacho", "email": "williampacho@example.com", "password": "12345"},
        {"id": 3, "username": "El lider", "email": "lidl@example.com", "password": "12345"},
        {"id": 4, "username": "Ares", "email": "ares@example.com", "password": "12345"}
    ]
    return users