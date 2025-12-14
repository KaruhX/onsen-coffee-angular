#!/bin/bash

echo "🔍 Verificando configuración para Vercel..."
echo ""

# Verificar archivos requeridos
echo "📁 Verificando archivos requeridos..."
files=("vercel.json" "requirements.txt" "api/index.py" "backend/main.py" ".python-version")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file existe"
    else
        echo "❌ $file NO encontrado"
    fi
done
echo ""

# Verificar estructura de directorios
echo "📂 Verificando estructura de directorios..."
dirs=("api" "backend" "backend/db" "backend/rest" "backend/admin" "backend/repository" "frontend")
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ existe"
    else
        echo "❌ $dir/ NO encontrado"
    fi
done
echo ""

# Verificar __init__.py
echo "🐍 Verificando módulos Python..."
init_files=("backend/__init__.py" "backend/db/__init__.py" "backend/rest/__init__.py" "backend/admin/__init__.py" "backend/repository/__init__.py")
for init in "${init_files[@]}"; do
    if [ -f "$init" ]; then
        echo "✅ $init existe"
    else
        echo "❌ $init NO encontrado"
    fi
done
echo ""

# Verificar dependencias
echo "📦 Verificando requirements.txt..."
if grep -q "Flask" requirements.txt && grep -q "Flask-Session" requirements.txt; then
    echo "✅ Dependencias principales encontradas"
else
    echo "⚠️  Verifica las dependencias en requirements.txt"
fi
echo ""

# Verificar Python version
echo "🐍 Versión de Python requerida:"
if [ -f ".python-version" ]; then
    cat .python-version
else
    echo "⚠️  No se encontró .python-version"
fi
echo ""

echo "✨ Verificación completada!"
echo ""
echo "🚀 Pasos para deploy en Vercel:"
echo "   1. git add ."
echo "   2. git commit -m 'Configuración para Vercel'"
echo "   3. git push origin master"
echo "   4. Conectar repositorio en vercel.com"
echo ""
