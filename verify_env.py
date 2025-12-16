#!/usr/bin/env python3
"""
Script para verificar que las variables de entorno estén configuradas correctamente
"""
import os
import sys

print("🔍 Verificando Variables de Entorno...\n")

required_vars = [
    'SUPABASE_URL',
    'SUPABASE_ANON_KEY',
    'SUPABASE_SERVICE_ROLE_KEY'
]

all_ok = True

for var in required_vars:
    value = os.environ.get(var)
    if value:
        # Mostrar solo los primeros 20 caracteres
        display_value = value[:20] + "..." if len(value) > 20 else value
        print(f"✅ {var}: {display_value}")
    else:
        print(f"❌ {var}: NO CONFIGURADA")
        all_ok = False

print("\n" + "="*60)

if all_ok:
    print("✅ Todas las variables están configuradas")
    print("\nProbando conexión a Supabase...")
    try:
        from backend.db.connection_supabase import get_supabase_client
        client = get_supabase_client()
        response = client.table('products').select('id').limit(1).execute()
        print(f"✅ Conexión a Supabase exitosa! ({len(response.data)} productos)")
    except Exception as e:
        print(f"❌ Error conectando a Supabase: {e}")
        sys.exit(1)
else:
    print("❌ Faltan variables de entorno")
    print("\nConfigúralas en Vercel:")
    print("https://vercel.com/tu-proyecto/settings/environment-variables")
    sys.exit(1)

print("="*60)
print("🎉 Todo configurado correctamente!")
