# Onsen Coffee
E-commerce de café de especialidad con Angular 21, Flask y SQLite.

## 🚀 Características

- **Frontend**: Angular 21 con Tailwind CSS y Material Icons
- **Backend**: Flask 3.0 con SQLite
- **Admin Panel**: Panel de administración con Material Design 3
- **Deployment**: Vercel

## 📁 Estructura del Proyecto

```
onsen-coffee/
├── frontend/          # Aplicación Angular
├── backend/           # API Flask
├── admin/             # Panel de administración
├── api/               # Vercel serverless functions
└── vercel.json        # Configuración de deployment
```

## 🏃‍♂️ Desarrollo Local

### Frontend
```bash
cd frontend
npm install
ng serve
# http://localhost:4200
```

### Backend API
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
# http://localhost:5000
```

### Admin Panel
```bash
cd admin
pip install -r requirements.txt
python app.py
# http://localhost:5001/admin
```

## 🌐 Deployment en Vercel

### 1. Configurar Variables de Entorno en Vercel
```bash
# En el dashboard de Vercel, agregar:
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
SUPABASE_DB_URL=postgresql://...
FLASK_SECRET_KEY=your-production-secret-key
```

### 2. Desplegar
```bash
vercel --prod
```

## 🎯 Ventajas de Supabase

✅ **Base de datos PostgreSQL** completa y escalable  
✅ **API REST automática** - No necesitas escribir endpoints CRUD  
✅ **Realtime** - Actualizaciones en tiempo real  
✅ **Authentication** - Sistema de autenticación integrado  
✅ **Storage** - Almacenamiento de archivos (imágenes de productos)  
✅ **Backups automáticos** - Tus datos están seguros  
✅ **500MB gratis** - Suficiente para empezar  
✅ **No hay servidor que mantener** - Totalmente serverless

## 📦 Scripts Útiles

- `npm run build` - Build del frontend
- `vercel dev` - Desarrollo local con Vercel
- `vercel --prod` - Deployment a producción

## 🎨 Admin Panel

El panel de administración incluye:
- ✅ Gestión de pedidos con estados (pending, processing, shipped, delivered, cancelled)
- ✅ Gestión de usuarios con roles (user, admin)
- ✅ Gestión de productos de café
- ✅ Material Design 3 con tema verde Onsen

**Nota**: En producción con SQLite, los cambios son temporales. Usa base de datos persistente.

## 📝 Licencia

MIT