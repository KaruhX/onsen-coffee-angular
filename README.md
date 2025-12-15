# ☕ Onsen Coffee

Una aplicación full-stack moderna para e-commerce de café de especialidad. Construida con Angular en el frontend y Flask en el backend.

## 🎯 Características

- **Catálogo de Cafés**: Visualiza una colección de cafés premium con detalles de origen, tueste y precio
- **Carrito de Compras**: Sistema completo de carrito con persistencia de sesión
- **Gestión de Pedidos**: Sistema de checkout y gestión de pedidos
- **Panel de Administración**: Gestión de productos y pedidos
- **API REST**: Backend robusto con Flask y SQLite
- **Deploy en Vercel**: Configurado para deployment serverless

## 📁 Estructura del Proyecto

```
onsen-coffee/
├── api/
│   └── index.py                # Entry point para Vercel
├── backend/
│   ├── main.py                 # Aplicación Flask principal
│   ├── db/
│   │   ├── connection.py       # Gestión de conexiones SQLite
│   │   └── schema.py           # Schema y datos seed
│   ├── repository/
│   │   └── store_repo.py       # Capa de acceso a datos
│   ├── rest/
│   │   └── app_rest.py         # Rutas de API REST
│   └── admin/
│       └── admin.py            # Rutas de administración
├── frontend/
│   └── src/
│       └── app/
│           ├── components/
│           │   ├── coffees/    # Catálogo de productos
│           │   ├── cart/       # Carrito de compras
│           │   ├── checkout/   # Proceso de pago
│           │   └── users/      # Gestión de usuarios
│           └── services/
│               ├── coffee-service.ts
│               └── user-service.ts
├── vercel.json                 # Configuración de Vercel
├── requirements.txt            # Dependencias Python
└── package.json                # Scripts de build
```

## 🚀 Instalación y Ejecución Local

### Backend (Python Flask)



1. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

2. **Ejecutar servidor**
```bash
cd backend
python main.py
```

El servidor estará disponible en `http://localhost:5000`

### Frontend (Angular)

1. **Instalar dependencias**
```bash
cd frontend
npm install
```

2. **Ejecutar servidor de desarrollo**
```bash
npm start
```

La aplicación estará disponible en `http://localhost:4200`

## 🌐 Deploy en Vercel

### Requisitos Previos
- Cuenta en Vercel
- Repositorio Git (GitHub, GitLab, Bitbucket)

### Pasos para Deploy

1. **Push del código a tu repositorio**
```bash
git add .
git commit -m "Configuración para Vercel"
git push origin master
```

2. **Importar proyecto en Vercel**
   - Ve a [vercel.com](https://vercel.com)
   - Click en "Add New Project"
   - Selecciona tu repositorio
   - Vercel detectará automáticamente la configuración de `vercel.json`

3. **Configuración automática**
   - El frontend Angular se construirá automáticamente
   - El backend Flask se desplegará como función serverless
   - La base de datos SQLite se inicializará en `/tmp` en cada invocación

### Notas sobre el Deploy

⚠️ **Importante**: SQLite en Vercel es **efímero** (se reinicia con cada despliegue). 

**Recomendaciones para producción:**
- Usar PostgreSQL, MySQL o MongoDB
- Considerar Vercel Postgres o Supabase
- Para desarrollo/demo, SQLite funciona pero los datos se pierden entre deploys

### Estructura de Deploy

- **Frontend**: Se sirve desde `/` (archivo estático)
- **Backend API**: Se sirve desde `/api/*` (función serverless)
- **Base de datos**: SQLite en `/tmp` (efímero)

## 🔌 Endpoints de API

### Cafés
- `GET /api/coffees` - Obtener catálogo de cafés
- `GET /api/coffees/:id` - Obtener café por ID

### Carrito
- `GET /api/cart` - Obtener carrito actual
- `POST /api/cart` - Agregar producto al carrito
- `PUT /api/cart/:id` - Actualizar cantidad
- `DELETE /api/cart/:id` - Eliminar producto
- `DELETE /api/cart` - Vaciar carrito

### Pedidos
- `POST /api/orders` - Crear nuevo pedido
- `GET /api/orders/:id` - Obtener pedido por ID
- `GET /api/orders/by-email/:email` - Obtener pedidos por email
- `GET /api/orders` - Obtener todos los pedidos (admin)
- `PUT /api/orders/:id/status` - Actualizar estado de pedido

### Usuarios
- `GET /api/users` - Obtener lista de usuarios

## 🎨 Tecnologías Utilizadas

### Frontend
- **Angular 21** - Framework principal
- **TypeScript** - Lenguaje de programación
- **Tailwind CSS** - Estilos responsivos
- **RxJS** - Programación reactiva
- **Signals** - Sistema de reactividad moderno

### Backend
- **Python 3.9** - Lenguaje
- **Flask 3.0** - Framework web
- **Flask-Session** - Manejo de sesiones
- **SQLite** - Base de datos
- **Vercel** - Platform de deployment

## 📊 Schema de Base de Datos

### Tablas Principales
- **users**: Usuarios del sistema (clientes y admins)
- **products**: Catálogo de cafés
- **orders**: Pedidos realizados
- **order_items**: Items de cada pedido

### Datos Seed
El sistema incluye datos de ejemplo:
- 5 usuarios (1 admin, 4 clientes)
- 8 productos de café de diferentes orígenes
- Imágenes de Unsplash para cada producto

## 🔧 Configuración del Proxy (Desarrollo Local)

El archivo `frontend/proxy.conf.json` redirige automáticamente las llamadas a `/api` hacia `http://localhost:5000` durante el desarrollo.

```json
{
  "/api": {
    "target": "http://localhost:5000",
    "secure": false,
    "changeOrigin": true
  }
}
```

## 📝 Archivos de Configuración Importantes

- `vercel.json`: Configuración de deploy en Vercel
- `.vercelignore`: Archivos excluidos del deploy
- `.python-version`: Versión de Python para Vercel
- `requirements.txt`: Dependencias de Python
- `package.json`: Scripts de build para el proyecto

## 🔐 Variables de Entorno (Opcional)

Para producción, puedes configurar:
- `SECRET_KEY`: Clave secreta para Flask
- `DATABASE_URL`: URL de base de datos externa (PostgreSQL, etc.)

## 🐛 Troubleshooting

### Error: "Module not found"
- Verifica que todos los `__init__.py` existan
- Revisa que `sys.path` incluya el directorio backend

### Error: "Database is locked"
- En Vercel, cada función serverless tiene su propia instancia
- Usa `check_same_thread=False` en SQLite (ya configurado)

### Frontend no carga el API
- Verifica que las rutas en `vercel.json` estén correctas
- Revisa los logs de Vercel para errores del backend

# Onsen Coffee

## Despliegue en Vercel

### Configuración Inicial

1. **Variables de Entorno en Vercel:**
   ```
   DATABASE_URL=tu_postgresql_url
   SECRET_KEY=tu_clave_secreta
   ```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

### Estructura del Proyecto

```
onsen-coffee/
├── src/                    # Frontend Next.js
├── admin/                  # Backend Flask Admin
│   ├── app.py             # Aplicación Flask
│   ├── templates/         # Templates HTML
│   ├── requirements.txt   # Dependencias Python
│   └── vercel.json       # Config Vercel Python
├── prisma/               # Base de datos
└── vercel.json          # Config principal Vercel
```

### Rutas Admin

- `/admin` - Dashboard principal
- `/admin/register-coffee` - Crear producto
- `/admin/update/<id>` - Editar producto
- `/admin/coffees` - Lista de productos
- `/admin/api/*` - API endpoints

### Características Admin

✅ Gestión de Pedidos (CRUD)  
✅ Gestión de Usuarios (CRUD)  
✅ Gestión de Productos (CRUD)  
✅ Dashboard con pestañas  
✅ Diseño Material consistente  
✅ Responsive design  

## 📄 Licencia

MIT - Libre para usar y modificar

---

**Hecho con ☕ por el equipo de Onsen Coffee**

