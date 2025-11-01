# Backend Gestor de inventario
gestor de inventario con login, permisos segun tipo de usuario. Con control de provedores, clientes frecuentes y materia prima

backend/
│
├── app/
│   ├── __init__.py
│   │
│   ├── main.py                 # Punto de entrada de la aplicación
│   │
│   ├── core/                   # Configuración central
│   │   ├── __init__.py
│   │   ├── config.py          # Variables de entorno y configuración
│   │   ├── security.py        # Funciones de seguridad (JWT, hashing)
│   │   └── dependencies.py    # Dependencias globales
│   │
│   ├── api/                    # Capa de API
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependencias compartidas de endpoints
│   │   └── v1/                # Versión 1 de la API
│   │       ├── __init__.py
│   │       ├── router.py      # Router principal que agrupa todos
│   │       └── endpoints/     # Endpoints específicos
│   │           ├── __init__.py
│   │           ├── auth.py    # Login, registro
│   │           ├── users.py   # CRUD de usuarios
│   │           ├── posts.py   # CRUD de posts
│   │           └── comments.py
│   │
│   ├── models/                 # Modelos de base de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   │
│   ├── schemas/                # Schemas de validación (Pydantic)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── token.py
│   │
│   ├── crud/                   # Operaciones CRUD
│   │   ├── __init__.py
│   │   ├── base.py            # CRUD genérico base
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   │
│   ├── db/                     # Base de datos
│   │   ├── __init__.py
│   │   ├── base.py            # Importa todos los modelos
│   │   ├── session.py         # Configuración de sesión
│   │   └── init_db.py         # Inicialización de BD
│   │
│   └── utils/                  # Utilidades
│       ├── __init__.py
│       └── email.py           # Funciones auxiliares
│
├── alembic/                    # Migraciones de base de datos
│   ├── versions/
│   └── env.py
│
├── tests/                      # Tests
│   ├── __init__.py
│   ├── conftest.py
│   └── api/
│
├── .env                        # Variables de entorno
├── .env.example               # Ejemplo de variables
├── alembic.ini                # Configuración de Alembic
├── requirements.txt           # Dependencias
└── README.md
```

---

## 🎯 Explicación de Cada Carpeta/Archivo

### **`app/main.py`**
- **Propósito**: Punto de entrada de la aplicación
- **Contiene**: Inicialización de FastAPI, CORS, routers principales
- **Ejemplo de contenido**: 
  - Crear instancia de FastAPI
  - Configurar middleware
  - Incluir routers

### **`app/core/`** - El Corazón de la Configuración
- **`config.py`**: Variables de entorno (DATABASE_URL, SECRET_KEY, etc.)
- **`security.py`**: Funciones de seguridad (crear tokens, verificar passwords)
- **`dependencies.py`**: Dependencias que se usan en múltiples lugares

### **`app/api/`** - Capa de Presentación
- Aquí viven todos tus endpoints REST
- **`v1/`**: Versión 1 de tu API (facilita versionado futuro)
- **`endpoints/`**: Cada archivo es un recurso (users, posts, etc.)
- Cada endpoint usa los schemas para validar input/output

### **`app/models/`** - Modelos de Base de Datos
- Define la **estructura de tus tablas**
- Usa SQLAlchemy ORM
- Ejemplo: `class User(Base)` con columnas como id, email, password

### **`app/schemas/`** - Validación de Datos
- Define qué datos **entran y salen** de tu API
- Usa Pydantic
- Ejemplo: `UserCreate` (lo que recibes), `UserResponse` (lo que devuelves)

### **`app/crud/`** - Lógica de Negocio
- Funciones que **interactúan con la base de datos**
- Separa la lógica de los endpoints
- Ejemplo: `create_user()`, `get_user_by_email()`

### **`app/db/`** - Configuración de Base de Datos
- **`session.py`**: Crea conexiones a la BD
- **`base.py`**: Importa todos los modelos (importante para Alembic)

---

## 🏛️ Patrón de Diseño: **Arquitectura en Capas (Layered Architecture)**

### ¿Por qué este patrón?

**Estamos usando una arquitectura en capas con elementos de Clean Architecture**. Aquí está el flujo:
```
Request → API Layer → CRUD Layer → Database
         ↓           ↓
      Schemas    Models
```

### **Ventajas de esta arquitectura:**

1. **Separación de responsabilidades**: Cada capa tiene un propósito claro
   - API: Recibe requests, valida, responde
   - CRUD: Lógica de negocio y operaciones DB
   - Models: Estructura de datos
   - Schemas: Validación y serialización

2. **Testeable**: Puedes testear cada capa independientemente

3. **Mantenible**: Si cambias la base de datos, solo modificas CRUD y Models

4. **Escalable**: Fácil agregar nuevas funcionalidades sin romper lo existente

5. **Reutilizable**: La lógica CRUD se puede usar desde diferentes endpoints

### **Flujo de una Request típica:**
```
1. Usuario hace POST /api/v1/users
2. El endpoint en api/v1/endpoints/users.py recibe la request
3. Usa el schema UserCreate para validar los datos
4. Llama a crud.user.create() pasando los datos validados
5. CRUD interactúa con el modelo User y la base de datos
6. Devuelve el objeto creado
7. El endpoint lo serializa con UserResponse schema
8. FastAPI devuelve JSON al cliente