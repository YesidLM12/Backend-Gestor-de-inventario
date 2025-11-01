# Backend Gestor de inventario
gestor de inventario con login, permisos segun tipo de usuario. Con control de provedores, clientes frecuentes y materia prima

backend/    # 🏗️ CARPETA PRINCIPAL DEL PROYECTO
│  
├── app/    # 🏛️ CARPETA DE LA APLICACIÓN       
│   ├── __init__.py     
│   │   └── 📝 Marca el directorio como paquete Python      
│   │    
│   ├── main.py      
│   │   └── 🎯 PUNTO DE ENTRADA de la aplicación   
│   │       ├── Crea la instancia de FastAPI    
│   │       ├── Configura CORS y middleware     
│   │       ├── Incluye todos los routers (auth, users, suppliers, etc.)      
│   │       └── Maneja eventos de startup/shutdown    
│   │    
│   ├── core/                   # 🏛️ CONFIGURACIÓN CENTRAL  
│   │   ├── __init__.py    
│   │   │      
│   │   ├── config.py      
│   │   │   └── ⚙️ Variables de entorno y configuración global    
│   │   │       ├── DATABASE_URL (conexión a PostgreSQL/MySQL)    
│   │   │       ├── SECRET_KEY (para JWT)    
│   │   │       ├── ALGORITHM (HS256 para tokens)     
│   │   │       ├── ACCESS_TOKEN_EXPIRE_MINUTES    
│   │   │       └── Configuraciones de CORS, logs, etc.     
│   │   │      
│   │   ├── security.py    
│   │   │   └── 🔐 Funciones de seguridad    
│   │   │       ├── hash_password() - Hashear contraseñas con bcrypt    
│   │   │       ├── verify_password() - Verificar contraseña vs hash    
│   │   │       ├── create_access_token() - Generar JWT     
│   │   │       └── decode_token() - Decodificar y validar JWT    
│   │   │      
│   │   ├── dependencies.py      
│   │   │   └── 🔗 Dependencias globales reutilizables      
│   │   │       ├── get_db() - Obtener sesión de base de datos    
│   │   │       ├── get_current_user() - Extraer usuario del token      
│   │   │       └── Otras dependencias compartidas    
│   │   │      
│   │   └── permissions.py          # 🆕 NUEVO      
│   │       └── 👮 Sistema de roles y permisos     
│   │           ├── Enum de roles (ADMIN, MANAGER, OPERATOR, VIEWER)    
│   │           ├── require_role() - Decorador para proteger endpoints     
│   │           ├── has_permission() - Verificar permisos específicos      
│   │           └── Matriz de permisos por rol     
│   │          
│   ├── api/                    # 🌐 CAPA DE API (Endpoints HTTP)     
│   │   ├── __init__.py          
│   │   │
│   │   ├── deps.py             # 🔌 Dependencias específicas de la API    
│   │   │       ├── get_current_active_user() - Usuario activo    
│   │   │       ├── verify_admin() - Verificar si es admin     
│   │   │       ├── verify_manager() - Verificar si es manager    
│   │   │       └── Dependencias de paginación     
│   │   │      
│   │   └── v1/                 # 📦 Versión 1 de la API    
│   │       ├── __init__.py      
│   │       │     
│   │       ├── router.py     
│   │       │   └── 🚦 Router principal (agrupa todos los endpoints)    
│   │       │       ├── Incluye auth.router     
│   │       │       ├── Incluye users.router    
│   │       │       ├── Incluye suppliers.router      
│   │       │       └── etc. (todos los endpoints)    
│   │       │     
│   │       └── endpoints/      # 🎯 ENDPOINTS específicos por recurso     
│   │           ├── __init__.py     
│   │           │    
│   │           ├── auth.py      
│   │           │   └── 🔑 Autenticación     
│   │           │       ├── POST /login - Iniciar sesión (devuelve JWT)    
│   │           │       ├── POST /register - Registrar nuevo usuario    
│   │           │       ├── POST /refresh - Refrescar token    
│   │           │       └── POST /logout - Cerrar sesión    
│   │           │    
│   │           ├── users.py     
│   │           │   └── 👤 Gestión de usuarios     
│   │           │       ├── GET /users - Listar usuarios (paginado)     
│   │           │       ├── GET /users/{id} - Obtener usuario específico      
│   │           │       ├── GET /users/me - Usuario actual     
│   │           │       ├── PUT /users/{id} - Actualizar usuario     
│   │           │       ├── DELETE /users/{id} - Eliminar usuario    
│   │           │       └── PUT /users/{id}/role - Cambiar rol (solo admin)      
│   │           │    
│   │           ├── suppliers.py        # 🆕 NUEVO     
│   │           │   └── 🏭 Gestión de proveedores     
│   │           │       ├── GET /suppliers - Listar proveedores      
│   │           │       ├── GET /suppliers/{id} - Obtener proveedor     
│   │           │       ├── POST /suppliers - Crear proveedor (manager+)      
│   │           │       ├── PUT /suppliers/{id} - Actualizar proveedor     
│   │           │       ├── DELETE /suppliers/{id} - Eliminar proveedor    
│   │           │       └── GET /suppliers/{id}/materials - Materiales del proveedor      
│   │           │    
│   │           ├── customers.py        # 🆕 NUEVO     
│   │           │   └── 🛒 Gestión de clientes frecuentes      
│   │           │       ├── GET /customers - Listar clientes      
│   │           │       ├── GET /customers/{id} - Obtener cliente    
│   │           │       ├── POST /customers - Crear cliente    
│   │           │       ├── PUT /customers/{id} - Actualizar cliente    
│   │           │       ├── DELETE /customers/{id} - Eliminar cliente      
│   │           │       └── GET /customers/{id}/orders - Órdenes del cliente     
│   │           │    
│   │           ├── raw_materials.py    # 🆕 NUEVO     
│   │           │   └── 📦 Catálogo de materia prima     
│   │           │       ├── GET /raw-materials - Listar materiales      
│   │           │       ├── GET /raw-materials/{id} - Obtener material     
│   │           │       ├── POST /raw-materials - Crear material (manager+)      
│   │           │       ├── PUT /raw-materials/{id} - Actualizar material     
│   │           │       ├── DELETE /raw-materials/{id} - Eliminar material    
│   │           │       └── GET /raw-materials/{id}/stock - Ver stock actual     
│   │           │    
│   │           ├── inventory.py        # 🆕 NUEVO     
│   │           │   └── 📊 Control de stock y movimientos      
│   │           │       ├── GET /inventory - Ver todo el inventario     
│   │           │       ├── GET /inventory/{material_id} - Stock de un material     
│   │           │       ├── POST /inventory/entrada - Registrar entrada    
│   │           │       ├── POST /inventory/salida - Registrar salida      
│   │           │       ├── POST /inventory/ajuste - Ajuste de inventario     
│   │           │       ├── GET /inventory/low-stock - Materiales con stock bajo    
│   │           │       └── GET /inventory/movements - Historial de movimientos     
│   │           │    
│   │           └── reports.py          # 🆕 NUEVO     
│   │               └── 📈 Reportes y estadísticas    
│   │                   ├── GET /reports/inventory-value - Valor total inventario      
│   │                   ├── GET /reports/movements - Reporte de movimientos      
│   │                   ├── GET /reports/suppliers - Top proveedores    
│   │                   ├── GET /reports/customers - Top clientes    
│   │                   └── GET /reports/dashboard - Datos para dashboard     
│   │    
│   ├── models/                 # 🗄️ MODELOS DE BASE DE DATOS (SQLAlchemy ORM)      
│   │   ├── __init__.py    
│   │   │   └── Exporta todos los modelos    
│   │   │      
│   │   ├── user.py     
│   │   │   └── 👤 Modelo Usuario      
│   │   │       ├── Campos: id, email, hashed_password, full_name, role    
│   │   │       ├── role: Enum(ADMIN, MANAGER, OPERATOR, VIEWER)     
│   │   │       ├── is_active: Boolean    
│   │   │       ├── created_at, updated_at: DateTime     
│   │   │       └── Relaciones: movements (movimientos que hizo)     
│   │   │      
│   │   ├── supplier.py         # 🆕 NUEVO    
│   │   │   └── 🏭 Modelo Proveedor    
│   │   │       ├── Campos: id, name, contact_name, phone, email, address     
│   │   │       ├── tax_id: Identificación fiscal     
│   │   │       ├── is_active: Boolean    
│   │   │       ├── created_at, updated_at      
│   │   │       └── Relaciones: raw_materials (many-to-many)      
│   │   │      
│   │   ├── customer.py         # 🆕 NUEVO    
│   │   │   └── 🛒 Modelo Cliente Frecuente     
│   │   │       ├── Campos: id, name, contact_name, phone, email, address     
│   │   │       ├── discount_percentage: Descuento aplicable      
│   │   │       ├── credit_limit: Límite de crédito      
│   │   │       ├── is_active: Boolean    
│   │   │       └── Relaciones: orders (órdenes del cliente)      
│   │   │      
│   │   ├── raw_material.py     # 🆕 NUEVO    
│   │   │   └── 📦 Modelo Materia Prima      
│   │   │       ├── Campos: id, name, code (SKU), description     
│   │   │       ├── unit_of_measure: Enum(KG, L, UNIDAD, M, etc.)    
│   │   │       ├── unit_price: Decimal (precio unitario)      
│   │   │       ├── min_stock: Stock mínimo (alerta)     
│   │   │       ├── max_stock: Stock máximo     
│   │   │       ├── is_active: Boolean    
│   │   │       └── Relaciones:     
│   │   │           ├── suppliers (many-to-many)      
│   │   │           ├── inventory (one-to-one)     
│   │   │           └── movements (historial)      
│   │   │      
│   │   ├── inventory.py        # 🆕 NUEVO    
│   │   │   └── 📊 Modelo Inventario (Stock Actual)      
│   │   │       ├── Campos: id, raw_material_id (FK)     
│   │   │       ├── quantity: Decimal (cantidad actual)     
│   │   │       ├── location: String (ubicación física)     
│   │   │       ├── last_updated: DateTime      
│   │   │       └── Relaciones: raw_material (one-to-one)      
│   │   │      
│   │   ├── movement.py         # 🆕 NUEVO    
│   │   │   └── 📝 Modelo Movimiento (Historial)      
│   │   │       ├── Campos: id, raw_material_id (FK)     
│   │   │       ├── type: Enum(ENTRADA, SALIDA, AJUSTE, MERMA)    
│   │   │       ├── quantity: Decimal     
│   │   │       ├── quantity_before: Decimal (stock antes)     
│   │   │       ├── quantity_after: Decimal (stock después)    
│   │   │       ├── reference: String (número de orden, etc.)     
│   │   │       ├── notes: Text (observaciones)    
│   │   │       ├── user_id: FK (quién lo hizo)    
│   │   │       ├── created_at: DateTime     
│   │   │       └── Relaciones: user, raw_material    
│   │   │      
│   │   └── supplier_material.py # 🆕 NUEVO      
│   │       └── 🔗 Tabla intermedia (Many-to-Many)    
│   │           ├── supplier_id: FK    
│   │           ├── raw_material_id: FK      
│   │           ├── supplier_price: Decimal (precio del proveedor)      
│   │           ├── is_preferred: Boolean (proveedor preferido)      
│   │           └── last_purchase_date: DateTime      
│   │    
│   ├── schemas/                # 📋 SCHEMAS DE VALIDACIÓN (Pydantic)      
│   │   ├── __init__.py    
│   │   │   └── Define qué datos ENTRAN y SALEN de la API      
│   │   │      
│   │   ├── user.py     
│   │   │   └── 👤 Schemas de Usuario     
│   │   │       ├── UserBase: Campos comunes (email, full_name)      
│   │   │       ├── UserCreate: Para crear (+ password)     
│   │   │       ├── UserUpdate: Para actualizar (campos opcionales)     
│   │   │       ├── UserResponse: Lo que se devuelve (sin password)     
│   │   │       └── UserInDB: Representación interna     
│   │   │      
│   │   ├── token.py    
│   │   │   └── 🎫 Schemas de Tokens JWT     
│   │   │       ├── Token: {access_token, token_type}    
│   │   │       ├── TokenData: Datos dentro del token    
│   │   │       └── RefreshToken    
│   │   │      
│   │   ├── supplier.py         # 🆕 NUEVO    
│   │   │   └── 🏭 Schemas de Proveedor      
│   │   │       ├── SupplierBase, SupplierCreate, SupplierUpdate     
│   │   │       └── SupplierResponse (incluye materiales relacionados)     
│   │   │      
│   │   ├── customer.py         # 🆕 NUEVO    
│   │   │   └── 🛒 Schemas de Cliente     
│   │   │       ├── CustomerBase, CustomerCreate, CustomerUpdate     
│   │   │       └── CustomerResponse      
│   │   │      
│   │   ├── raw_material.py     # 🆕 NUEVO    
│   │   │   └── 📦 Schemas de Materia Prima     
│   │   │       ├── RawMaterialBase, RawMaterialCreate, RawMaterialUpdate     
│   │   │       └── RawMaterialResponse (incluye stock actual)    
│   │   │      
│   │   ├── inventory.py        # 🆕 NUEVO    
│   │   │   └── 📊 Schemas de Inventario     
│   │   │       ├── InventoryResponse: Stock actual de un material      
│   │   │       ├── StockAdjust: Para ajustes manuales      
│   │   │       └── LowStockAlert: Materiales con stock bajo      
│   │   │      
│   │   ├── movement.py         # 🆕 NUEVO    
│   │   │   └── 📝 Schemas de Movimientos    
│   │   │       ├── MovementCreate: Registrar entrada/salida      
│   │   │       ├── MovementResponse: Historial de movimiento     
│   │   │       └── MovementFilter: Filtros para consultas     
│   │   │      
│   │   └── common.py           # 🆕 NUEVO    
│   │       └── 🔧 Schemas comunes reutilizables      
│   │           ├── PaginationParams: skip, limit     
│   │           ├── DateRangeFilter: desde, hasta     
│   │           ├── MessageResponse: {message: "OK"}     
│   │           └── ErrorResponse: {detail: "error"}     
│   │    
│   ├── crud/                   # 🔨 OPERACIONES CRUD (Lógica de negocio)     
│   │   ├── __init__.py    
│   │   │   └── Funciones que INTERACTÚAN con la base de datos    
│   │   │      
│   │   ├── base.py     
│   │   │   └── 🏗️ CRUD genérico base (clase abstracta)     
│   │   │       ├── get(id) - Obtener por ID    
│   │   │       ├── get_multi(skip, limit) - Listar paginado      
│   │   │       ├── create(obj_in) - Crear registro      
│   │   │       ├── update(id, obj_in) - Actualizar      
│   │   │       └── delete(id) - Eliminar    
│   │   │      
│   │   ├── user.py     
│   │   │   └── 👤 CRUD de Usuario (hereda de base)      
│   │   │       ├── get_by_email(email) - Buscar por email     
│   │   │       ├── authenticate(email, password) - Verificar login     
│   │   │       ├── get_by_role(role) - Filtrar por rol     
│   │   │       └── update_role(id, new_role) - Cambiar rol    
│   │   │      
│   │   ├── supplier.py         # 🆕 NUEVO    
│   │   │   └── 🏭 CRUD de Proveedor      
│   │   │       ├── get_active() - Solo proveedores activos    
│   │   │       ├── get_with_materials(id) - Con materiales relacionados      
│   │   │       └── search_by_name(name) - Búsqueda por nombre    
│   │   │      
│   │   ├── customer.py         # 🆕 NUEVO    
│   │   │   └── 🛒 CRUD de Cliente     
│   │   │       ├── get_active() - Solo clientes activos    
│   │   │       ├── get_by_credit_limit(min, max) - Filtrar por crédito    
│   │   │       └── calculate_total_purchases(id) - Total comprado      
│   │   │      
│   │   ├── raw_material.py     # 🆕 NUEVO    
│   │   │   └── 📦 CRUD de Materia Prima     
│   │   │       ├── get_by_code(code) - Buscar por SKU      
│   │   │       ├── get_with_stock(id) - Con información de stock    
│   │   │       ├── assign_supplier(material_id, supplier_id) - Relacionar    
│   │   │       └── get_low_stock() - Materiales con stock bajo      
│   │   │      
│   │   ├── inventory.py        # 🆕 NUEVO - ⚠️ LÓGICA COMPLEJA    
│   │   │   └── 📊 CRUD de Inventario (operaciones críticas)      
│   │   │       ├── get_stock(material_id) - Stock actual      
│   │   │       ├── adjust_stock(material_id, quantity, type) - Ajustar stock    
│   │   │       ├── register_entry(material_id, quantity, user_id) - Entrada     
│   │   │       ├── register_exit(material_id, quantity, user_id) - Salida    
│   │   │       ├── validate_availability(material_id, quantity) - Verificar stock     
│   │   │       ├── get_inventory_value() - Valor total del inventario     
│   │   │       └── get_movements_history(filters) - Historial    
│   │   │      
│   │   └── movement.py         # 🆕 NUEVO    
│   │       └── 📝 CRUD de Movimientos    
│   │           ├── create_movement(data) - Registrar movimiento     
│   │           ├── get_by_material(material_id) - Historial de un material      
│   │           ├── get_by_user(user_id) - Movimientos por usuario      
│   │           ├── get_by_date_range(start, end) - Por rango de fechas    
│   │           └── get_by_type(type) - Por tipo (ENTRADA, SALIDA, etc.)      
│   │    
│   ├── db/                     # 💾 CONFIGURACIÓN DE BASE DE DATOS     
│   │   ├── __init__.py    
│   │   │      
│   │   ├── base.py     
│   │   │   └── 📚 Importa TODOS los modelos    
│   │   │       ├── Necesario para que Alembic detecte cambios    
│   │   │       └── Importa User, Supplier, Customer, etc.     
│   │   │      
│   │   ├── session.py     
│   │   │   └── 🔌 Configuración de conexión a BD     
│   │   │       ├── engine = create_engine(DATABASE_URL)    
│   │   │       ├── SessionLocal = sessionmaker(engine)     
│   │   │       └── Base = declarative_base()      
│   │   │      
│   │   └── init_db.py     
│   │       └── 🌱 Inicialización y datos semilla (seed data)     
│   │           ├── Crear usuario ADMIN por defecto      
│   │           ├── Crear categorías básicas    
│   │           └── Datos de prueba (opcional)     
│   │    
│   └── utils/                  # 🛠️ UTILIDADES Y HELPERS      
│       ├── __init__.py    
│       │      
│       ├── enums.py            # 🆕 NUEVO    
│       │   └── 📝 Enumeraciones del sistema    
│       │       ├── UserRole(ADMIN, MANAGER, OPERATOR, VIEWER)    
│       │       ├── MovementType(ENTRADA, SALIDA, AJUSTE, MERMA)     
│       │       ├── UnitOfMeasure(KG, L, UNIDAD, M, M2, M3)    
│       │       └── OrderStatus(PENDING, APPROVED, COMPLETED, CANCELLED)      
│       │      
│       ├── validators.py       # 🆕 NUEVO    
│       │   └── ✅ Validaciones custom de negocio     
│       │       ├── validate_positive_quantity() - Cantidad > 0      
│       │       ├── validate_stock_availability() - Hay suficiente stock?     
│       │       ├── validate_email_format() - Email válido     
│       │       └── validate_phone_format() - Teléfono válido     
│       │      
│       └── exceptions.py       # 🆕 NUEVO       
│           └── ❌ Excepciones personalizadas      
│               ├── InsufficientStockException     
│               ├── InvalidMovementException    
│               ├── DuplicateRecordException    
│               └── PermissionDeniedException      
│
├── alembic/                    # 🔄 MIGRACIONES DE BASE DE DATOS    
│   ├── versions/               # Versiones de la BD     
│   │   ├── 001_initial_tables.py        # Tablas iniciales (users)     
│   │   ├── 002_add_user_roles.py        # Agregar roles a users     
│   │   └── 003_inventory_tables.py      # Tablas de inventario      
│   │    
│   ├── env.py                  # Configuración de Alembic     
│   └── script.py.mako          # Template para nuevas migraciones      
│     
├── tests/                      # 🧪 TESTS UNITARIOS E INTEGRACIÓN      
│   ├── __init__.py     
│   │    
│   ├── conftest.py     
│   │   └── 🔧 Fixtures compartidos (BD de prueba, cliente HTTP)     
│   │    
│   ├── api/                    # Tests de endpoints     
│   │   ├── test_auth.py        # Login, registro, tokens      
│   │   ├── test_users.py       # CRUD usuarios    
│   │   ├── test_suppliers.py   # 🆕 CRUD proveedores     
│   │   ├── test_inventory.py   # 🆕 Movimientos de inventario     
│   │   └── test_permissions.py # 🆕 Sistema de permisos     
│   │    
│   └── crud/                   # Tests de lógica de negocio      
│       ├── test_user_crud.py    
│       └── test_inventory_crud.py # 🆕 Lógica compleja de inventario    
│     
├── .env                        # 🔐 Variables de entorno (NO subir a git)    
│   ├── DATABASE_URL=postgresql://user:pass@localhost/inventory_db      
│   ├── SECRET_KEY=tu-clave-super-secreta    
│   ├── ALGORITHM=HS256    
│   └── ACCESS_TOKEN_EXPIRE_MINUTES=30    
│     
├── .env.example                # 📝 Ejemplo de variables (SÍ subir a git)    
│   └── Template para que otros desarrolladores sepan qué configurar    
│     
├── .gitignore                  # 🚫 Archivos ignorados por git      
│   ├── .env      
│   ├── __pycache__/    
│   ├── *.pyc     
│   └── venv/     
│     
├── alembic.ini                 # ⚙️ Configuración de Alembic     
│     
├── requirements.txt            # 📦 Dependencias del proyecto    
│   ├── fastapi==0.104.1      
│   ├── uvicorn[standard]==0.24.0      
│   ├── sqlalchemy==2.0.23    
│   ├── alembic==1.12.1    
│   ├── pydantic==2.5.0    
│   ├── python-jose[cryptography]==3.3.0  # Para JWT        
│   ├── passlib[bcrypt]==1.7.4            # Para hashear passwords      
│   ├── python-multipart==0.0.6           # Para forms      
│   ├── psycopg2-binary==2.9.9            # PostgreSQL driver     
│   └── pytest==7.4.3                     # Para tests      
│     
└── README.md                   # 📖 Documentación del proyecto      
    ├── Descripción del proyecto    
    ├── Cómo instalar y correr      
    ├── Estructura explicada     
    ├── Endpoints disponibles    
    └── Ejemplos de uso    