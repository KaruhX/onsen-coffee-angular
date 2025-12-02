# ☕ Onsen Coffee

Una aplicación full-stack moderna para gestionar un catálogo de cafés premium y usuarios. Construida con Angular en el frontend y Flask en el backend.

## 🎯 Características

- **Catálogo de Cafés**: Visualiza una colección de cafés premium con detalles de origen, tueste y precio
- **Gestión de Usuarios**: Ver y gestionar usuarios del sistema
- **Interfaz Moderna**: Diseño responsivo con Tailwind CSS
- **API REST**: Backend robusto con Flask
- **Proxy de Desarrollo**: Configuración automática de proxy para desarrollo local

## 📁 Estructura del Proyecto

```
onsen-coffee/
├── backend/
│   ├── main.py                 # Punto de entrada de Flask
│   ├── db/
│   │   ├── store_repo.py       # Datos simulados
│   │   └── __init__.py
│   └── rest/
│       ├── app_rest.py         # Rutas de API REST
│       └── __init__.py
│
├── frontend/
│   ├── angular.json            # Configuración de Angular
│   ├── package.json
│   ├── proxy.conf.json         # Configuración del proxy
│   └── src/
│       ├── app/
│       │   ├── app.routes.ts   # Rutas de la aplicación
│       │   ├── app.html
│       │   ├── app.config.ts   # Configuración global
│       │   ├── models.ts
│       │   ├── components/
│       │   │   ├── coffees/    # Componente de catálogo
│       │   │   ├── users/      # Componente de usuarios
│       │   │   └── cart/       # Componente de carrito
│       │   └── services/
│       │       ├── coffee-service.ts
│       │       └── user-service.ts
│       └── styles.css
│
└── README.md
```

## 🚀 Instalación y Ejecución

### Backend (Python Flask)

1. **Instalar dependencias**
```bash
cd backend
python -m pip install flask
```

2. **Ejecutar servidor**
```bash
python main.py
```

El servidor estará disponible en `http://localhost:5000`

### Frontend (Angular)

1. **Instalar dependencias**
```bash
cd frontend
npm install
# o con bun
bun install
```

2. **Ejecutar servidor de desarrollo**
```bash
ng serve
# o con bun
bun start
```

La aplicación estará disponible en `http://localhost:4200`

## 🔌 Endpoints de API

### Cafés
- `GET /api/coffees` - Obtener catálogo de cafés

### Usuarios
- `GET /api/users` - Obtener lista de usuarios

## 🎨 Tecnologías Utilizadas

### Frontend
- **Angular 16+** - Framework principal
- **TypeScript** - Lenguaje de programación
- **Tailwind CSS** - Estilos responsivos
- **RxJS** - Programación reactiva

### Backend
- **Python 3.14** - Lenguaje
- **Flask** - Framework web
- **JSON** - Formato de datos

## 📊 Datos de Ejemplo

### Cafés Disponibles
- Ethiopian Yirgacheffe - Etiopía
- Colombian Geisha - Panamá
- Kenyan AA - Kenia
- Indonesian Sumatra Mandheling - Indonesia
- Costa Rican Tarrazú - Costa Rica

### Usuarios
- Chivo Valencia
- William Pacho
- El lider
- Ares

## 🔧 Configuración del Proxy

El archivo `frontend/proxy.conf.json` redirige automáticamente las llamadas a `/api` hacia `http://localhost:5000` durante el desarrollo.

```json
{
  "/api": {
    "target": "http://localhost:5000",
    "secure": false,
    "pathRewrite": {
      "^/api": "/api"
    },
    "changeOrigin": true
  }
}
```

## 📝 Notas de Desarrollo

- El backend usa UTF-8 para soportar caracteres especiales en los nombres de los cafés
- Los componentes de Angular usan Signals para reactividad moderna
- Se usa CommonModule para las directivas estructurales (@for, @if)

## 🤝 Contribuciones

Este proyecto es parte de una aplicación de e-commerce de café premium.

## 📄 Licencia

MIT - Libre para usar y modificar

---

**Hecho con ☕ por el equipo de Onsen Coffee**
