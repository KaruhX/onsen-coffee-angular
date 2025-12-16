#!/usr/bin/env python3
"""
Script para inicializar la base de datos de Onsen Coffee en Supabase
Ejecutar: python init_db.py
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(__file__))

from backend.db.schema import create_tables, insert_seed_data

def main():
    print("🚀 Iniciando configuración de base de datos Supabase...")
    print("=" * 60)
    
    try:
        print("\n📊 Creando tablas...")
        create_tables()
        print("✅ Tablas creadas exitosamente!")
        
        print("\n🌱 Insertando datos de ejemplo...")
        insert_seed_data()
        print("✅ Datos insertados exitosamente!")
        
        print("\n" + "=" * 60)
        print("🎉 ¡Base de datos inicializada correctamente!")
        print("\n📋 Tablas creadas:")
        print("   • users (usuarios)")
        print("   • products (cafés)")
        print("   • orders (pedidos)")
        print("   • order_items (items de pedidos)")
        
        print("\n🎯 Próximos pasos:")
        print("   1. Verifica las tablas en: https://app.supabase.com")
        print("   2. Ejecuta el servidor: python backend/main.py")
        print("   3. Accede a: http://localhost:5000")
        
    except Exception as e:
        print("\n❌ Error al inicializar la base de datos:")
        print(f"   {str(e)}")
        print("\n💡 Verifica que:")
        print("   1. Has configurado las variables en el archivo .env")
        print("   2. Las credenciales de Supabase son correctas")
        print("   3. Tu proyecto de Supabase está activo")
        sys.exit(1)

if __name__ == '__main__':
    main()
