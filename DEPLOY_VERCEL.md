# 🚀 Despliegue en Vercel - Onsen Coffee

## 📋 Configuración de Variables de Entorno en Vercel

Ve a tu proyecto en Vercel → **Settings** → **Environment Variables** y agrega:

```env
SUPABASE_URL=https://kvylferkavxxgtsuxlmh.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2eWxmZXJrYXZ4eGd0c3V4bG1oIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc3Njk4NzEsImV4cCI6MjA2MzM0NTg3MX0.NWy4ZlzD7SXOxFO3HBNBab1BX_OvoDwDvfv7LGxHfh4
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt2eWxmZXJrYXZ4eGd0c3V4bG1oIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Nzc2OTg3MSwiZXhwIjoyMDYzMzQ1ODcxfQ.Ldm8p_k_vPfAIlQwCnwjf-x8BAoMuiwyUKvZE29a5RY
SECRET_KEY=tu-secret-key-super-segura-aqui
```

**IMPORTANTE**: Marca estas variables para todos los entornos (Production, Preview, Development)

## 🔄 Desplegar en Vercel

### Opción 1: Desde Dashboard de Vercel (Recomendado)

1. Ve a https://vercel.com/dashboard
2. Click en tu proyecto "onsen-coffee" (o importa desde GitHub si no existe)
3. El deploy se iniciará automáticamente al detectar el push

### Opción 2: Desde CLI

```bash
# Instalar Vercel CLI si no la tienes
npm i -g vercel

# En el directorio del proyecto
cd /home/karuh/Documentos/Nelson/onsen-coffee

# Login (si no lo has hecho)
vercel login

# Desplegar
vercel --prod
```

## ✅ Verificación Post-Deploy

Una vez desplegado, verifica:

1. **Frontend**: https://tu-proyecto.vercel.app
   - Debe cargar la interfaz de Angular
   
2. **API**: https://tu-proyecto.vercel.app/api/coffees
   - Debe devolver JSON con los productos de Supabase
   
3. **Admin**: https://tu-proyecto.vercel.app/admin
   - Panel de administración (si aplica)

## 🐛 Troubleshooting

### Si el API falla:

1. Verifica logs en Vercel: Dashboard → Functions → Logs
2. Confirma variables de entorno están configuradas
3. Revisa que las tablas en Supabase tengan la columna `is_active`

### Si Angular no carga:

1. Verifica que el build se completó: `frontend/dist/frontend/browser` existe
2. Revisa build logs en Vercel
3. Confirma que `vercel.json` apunta al directorio correcto

## 🎯 URLs Importantes

- **Proyecto Vercel**: https://vercel.com/tu-usuario/onsen-coffee
- **Supabase Dashboard**: https://app.supabase.com
- **Repository**: https://github.com/KaruhX/onsen-coffee-angular

## 🔐 Seguridad

⚠️ **NUNCA** subas las API keys al repositorio público. Usa siempre las Environment Variables de Vercel.

## 📊 Monitoreo

- **Logs de Vercel**: Real-time en Dashboard → Functions
- **Logs de Supabase**: Logs & SQL Editor en dashboard
- **Analytics**: Vercel Analytics (opcional)
