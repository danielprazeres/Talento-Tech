# Sistema de Gestión de Inventario - Talento Tech

<div align="center">

Un sistema completo de gestión de inventario desarrollado en Python con múltiples interfaces de usuario (consola, web y API). Incluye configuración completa con Docker y Make para facilitar el desarrollo y despliegue.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

</div>

## Inicio Rápido

### Con Docker (Recomendado)
```bash
# Navegar al directorio del proyecto
cd proyecto_final

# Levantar todos los servicios
make quick-start

# Acceder a las interfaces
# Web: http://localhost:8501
# API: http://localhost:8000
# Docs API: http://localhost:8000/docs
```

### Sin Docker
```bash
# Navegar al directorio del proyecto
cd proyecto_final

# Instalar dependencias
make install

# Ejecutar interfaz web
make run-web
```

## Capturas del Sistema

### Interfaz de Consola
La interfaz de terminal con colores y menús interactivos:

![Sistema Terminal](proyecto_final/img/9.%20sistema_terminal.png)

### Interfaz Web (Streamlit)

#### Pantalla de Inicio
Dashboard principal con métricas en tiempo real:

![Inicio](proyecto_final/img/1.%20inicio.png)

#### Registrar Productos
Formulario intuitivo para agregar nuevos productos:

![Registrar Producto](proyecto_final/img/2.%20registrar_producto.png)

#### Visualizar Inventario
Vista completa del inventario con filtros y ordenamiento:

![Ver Productos](proyecto_final/img/3.%20ver_productos.png)

#### Búsqueda de Productos
Sistema de búsqueda avanzada por múltiples criterios:

![Buscar Productos](proyecto_final/img/4.%20buscar_productos.png)

#### Actualizar Productos
Interfaz para modificar productos existentes:

![Actualizar Productos](proyecto_final/img/5.%20actualizar_productos.png)

#### Reportes y Estadísticas
Dashboard con gráficos interactivos y reportes:

![Reportes](proyecto_final/img/6.%20reportes.png)

### API REST (FastAPI)

#### Documentación Automática
Swagger UI con todos los endpoints documentados:

![FastAPI Docs](proyecto_final/img/7.%20fast_api.png)

#### Consultas API
Ejemplo de respuesta JSON de la API:

![Consulta API](proyecto_final/img/8.%20consulta_productos_api.png)

## Características Principales

### Funcionalidades del Sistema
- ✅ **Registrar nuevos productos** con validación de datos
- ✅ **Visualizar productos** registrados con formato tabular
- ✅ **Actualizar datos** de productos mediante ID
- ✅ **Eliminar productos** con confirmación de seguridad
- ✅ **Búsqueda avanzada** por ID, nombre o categoría
- ✅ **Reportes de stock bajo** con límites personalizables
- ✅ **Estadísticas del inventario** en tiempo real
- ✅ **Gráficos interactivos** con Plotly
- ✅ **API REST completa** con documentación automática

### Interfaces Disponibles
| Interfaz | Descripción | Puerto | Captura |
|----------|-------------|--------|---------|
| **Consola** | Terminal interactivo | - | [Ver imagen](proyecto_final/img/9.%20sistema_terminal.png) |
| **Web** | Aplicación Streamlit moderna | 8501 | [Ver imagen](proyecto_final/img/1.%20inicio.png) |
| **API** | FastAPI con documentación | 8000 | [Ver imagen](proyecto_final/img/7.%20fast_api.png) |

### Tecnologías Utilizadas
- **Backend**: Python 3.10, SQLite
- **Web UI**: Streamlit, Plotly
- **API**: FastAPI, Pydantic
- **Containerización**: Docker, Docker Compose
- **Automatización**: Make
- **Styling**: Colorama para terminal

## Estructura de la Base de Datos

### Tabla `productos`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Identificador único (autoincremental) |
| `nombre` | TEXT NOT NULL | Nombre del producto |
| `descripcion` | TEXT | Descripción detallada |
| `cantidad` | INTEGER NOT NULL | Cantidad disponible en stock |
| `precio` | REAL NOT NULL | Precio unitario |
| `categoria` | TEXT | Categoría del producto |

## Instalación y Configuración

### 📋 Requisitos Previos
- **Para uso local**: Python 3.8+ y pip
- **Para Docker**: Docker y Docker Compose
- **Opcional**: Make (para comandos simplificados)

### Métodos de Instalación

#### 1. Con Make (Recomendado)
```bash
# Navegar al directorio del proyecto
cd proyecto_final

# Ver todos los comandos disponibles
make help

# Instalación local completa
make dev-setup

# Solo instalar dependencias
make install
```

#### 2. Manual
```bash
# Navegar al directorio del proyecto
cd proyecto_final

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Guía de Uso

### Comandos Make Principales

```bash
# Desde el directorio proyecto_final/

# 📋 Ver ayuda completa
make help

# 🛠️ Desarrollo local
make run-web          # Interfaz web (puerto 8501)
make run-api          # API REST (puerto 8000)
make run-console      # Interfaz de consola
make test             # Ejecutar pruebas

# 🐳 Docker - Servicios individuales
make docker-run-web   # Web en Docker
make docker-run-api   # API en Docker
make docker-test      # Pruebas en Docker

# 🎼 Docker Compose - Todos los servicios
make quick-start      # Iniciar todo en segundo plano
make quick-stop       # Detener todo
make restart          # Reiniciar servicios
```

### 1. Interfaz de Consola
```bash
cd proyecto_final

# Local
make run-console

# Docker
make docker-run-console
```

**Características:**
- Menú interactivo con navegación numérica
- Colores y formato mejorado (con colorama)
- Validación de entrada de datos
- Confirmaciones para operaciones críticas

### 2. Interfaz Web (Streamlit)
```bash
cd proyecto_final

# Local
make run-web

# Docker Compose (recomendado)
make quick-start
```

**Características:**
- Dashboard con métricas en tiempo real
- Gráficos interactivos con Plotly
- Filtros y ordenamiento de datos
- Formularios validados
- Interfaz moderna y responsive

**URL**: `http://localhost:8501`

### 3. API REST (FastAPI)
```bash
cd proyecto_final

# Local
make run-api

# Docker Compose (recomendado)
make quick-start
```

**Características:**
- API RESTful completa
- Documentación automática con Swagger
- Validación de datos con Pydantic
- Manejo de errores HTTP estándar
- Soporte CORS para aplicaciones web

**URLs:**
- **API**: `http://localhost:8000`
- **Documentación**: `http://localhost:8000/docs`

## Docker y Contenedores

### Docker Compose (Recomendado para Producción)
```bash
cd proyecto_final

# Levantar todos los servicios
make quick-start

# Ver logs en tiempo real
make docker-compose-logs

# Detener servicios
make quick-stop
```

### Docker Individual
```bash
cd proyecto_final

# Construir imagen
make docker-build

# Ejecutar servicios específicos
make docker-run-api      # Solo API
make docker-run-web      # Solo Web
make docker-run-console  # Solo consola (interactivo)

# Limpiar contenedores
make docker-stop
make docker-clean
```

### Configuración de Volúmenes
- La base de datos se almacena en `./data/` (compartida entre contenedores)
- Los datos persisten entre reinicios de contenedores

## Documentación de la API

### Endpoints Principales

#### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/productos/` | Obtener todos los productos |
| `POST` | `/productos/` | Crear nuevo producto |
| `GET` | `/productos/{id}` | Obtener producto por ID |
| `PUT` | `/productos/{id}` | Actualizar producto |
| `DELETE` | `/productos/{id}` | Eliminar producto |

#### Búsquedas
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/productos/buscar/nombre/{nombre}` | Buscar por nombre |
| `GET` | `/productos/categoria/{categoria}` | Buscar por categoría |

#### Reportes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/reportes/stock-bajo/{limite}` | Productos con stock bajo |
| `GET` | `/estadisticas` | Estadísticas generales |

### Ejemplo de Uso de la API

#### Crear un producto
```bash
curl -X POST "http://localhost:8000/productos/" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Laptop Dell",
       "descripcion": "Laptop Dell Inspiron 15",
       "cantidad": 10,
       "precio": 750.00,
       "categoria": "Electrónicos"
     }'
```

#### Obtener todos los productos
```bash
curl -X GET "http://localhost:8000/productos/"
```

#### Obtener estadísticas
```bash
curl -X GET "http://localhost:8000/estadisticas"
```

## Estructura del Proyecto

```
Talento-Tech/
├── Clase 01/               # Ejercicios de clase
├── Clase 02/               # Ejercicios de clase
├── ...                     # Más clases
└── proyecto_final/         # PROYECTO PRINCIPAL
    ├── database.py         # Manejador de base de datos SQLite
    ├── inventario.py       # Lógica de negocio y operaciones CRUD
    ├── main.py             # Interfaz de consola
    ├── app_streamlit.py    # Interfaz web con Streamlit
    ├── api.py              # API REST con FastAPI
    ├── test_sistema.py     # Script de pruebas
    ├── requirements.txt    # Dependencias de Python
    ├── Dockerfile          # Configuración de contenedor Docker
    ├── docker-compose.yml  # Orquestación de servicios
    ├── .dockerignore       # Archivos excluidos de Docker
    ├── Makefile            # Comandos automatizados
    ├── README.md           # Documentación técnica
    ├── img/                # Capturas de pantalla
    ├── pedido/             # Solicitud del proyecto
    ├── data/               # Base de datos (generada automáticamente)
    └── inventario.db       # Base de datos SQLite (generada)
```

## Comandos Make Completos

<details>
<summary>Ver todos los comandos disponibles</summary>

```bash
# Ejecutar desde proyecto_final/

# Ayuda y información
make help                    # Mostrar todos los comandos
make info                    # Información del sistema

# Instalación y configuración
make install                 # Instalar en entorno virtual
make install-global          # Instalar globalmente
make dev-setup              # Configuración completa

# 🏃 Ejecución local
make run-console            # Interfaz de consola
make run-web               # Interfaz web
make run-api               # API REST
make test                  # Ejecutar pruebas

# Docker individual
make docker-build          # Construir imagen
make docker-run-api        # API en Docker
make docker-run-web        # Web en Docker
make docker-run-console    # Consola en Docker
make docker-test           # Pruebas en Docker
make docker-stop           # Detener contenedores
make docker-clean          # Limpiar Docker

# Docker Compose
make docker-compose-up     # Levantar servicios
make quick-start           # Iniciar en segundo plano
make quick-stop            # Detener servicios
make restart               # Reiniciar
make docker-compose-logs   # Ver logs

# Limpieza
make clean                 # Limpiar archivos temporales
make clean-venv           # Eliminar entorno virtual
```

</details>

## Características Técnicas

### Validaciones Implementadas
- **Nombres**: No pueden estar vacíos
- **Cantidades**: Deben ser números enteros no negativos
- **Precios**: Deben ser números decimales positivos mayores a 0
- **IDs**: Deben existir en la base de datos para operaciones de actualización/eliminación

### Manejo de Errores
- Validación de entrada de datos
- Manejo de excepciones SQLite
- Mensajes de error descriptivos
- Confirmaciones para operaciones destructivas

### Características de Docker
- Imagen multi-etapa optimizada
- Entrypoint inteligente que permite ejecutar diferentes servicios
- Volúmenes para persistencia de datos
- Red interna para comunicación entre servicios
- Configuración de entorno para desarrollo y producción

## Ejemplos de Uso Rápido

### Inicio Rápido para Desarrollo
```bash
# Navegar al proyecto
cd proyecto_final

# Configurar entorno completo
make dev-setup

# Iniciar interfaz web
make run-web
```

### Despliegue con Docker
```bash
# Navegar al proyecto
cd proyecto_final

# Levantar todos los servicios en producción
make quick-start

# Verificar que funcione
curl http://localhost:8000/estadisticas
```

### Ejecutar Pruebas
```bash
cd proyecto_final

# Pruebas locales
make test

# Pruebas en Docker
make docker-test
```

## Monitoreo y Logs

### Ver logs de servicios
```bash
cd proyecto_final

# Docker Compose
make docker-compose-logs

# Docker individual
docker logs inventario-api-container
docker logs inventario-web-container
```

### Verificar estado de servicios
```bash
cd proyecto_final

# Información del sistema
make info

# Estado de contenedores
docker ps

# Estado de servicios
curl http://localhost:8000/estadisticas
curl http://localhost:8501
```

## Notas Importantes

- La base de datos `inventario.db` se crea automáticamente en la primera ejecución
- En Docker, los datos se almacenan en el directorio `./data/` del host
- Las tres interfaces comparten la misma base de datos y lógica de negocio
- Todas las operaciones incluyen validación y manejo de errores
- Los servicios en Docker Compose están configurados para reiniciarse automáticamente
- **Todos los comandos deben ejecutarse desde el directorio `proyecto_final/`**

## Resolución de Problemas

### Problemas Comunes

<details>
<summary>Puerto ocupado</summary>

```bash
cd proyecto_final

# Cambiar puertos en docker-compose.yml
# O detener otros servicios
make docker-stop
```

</details>

<details>
<summary>Permisos en volúmenes</summary>

```bash
cd proyecto_final

# Crear directorio data con permisos correctos
mkdir -p data
chmod 755 data
```

</details>

<details>
<summary>Dependencias faltantes</summary>

```bash
cd proyecto_final

# Reinstalar dependencias
make clean
make dev-setup
```

</details>

### Comandos Útiles para Debugging
```bash
cd proyecto_final

# Limpiar todo y empezar de nuevo
make docker-clean
make clean
make quick-start

# Ver logs de errores
make docker-compose-logs

# Información completa del sistema
make info
```

## Soporte y Mantenimiento

Para reportar problemas:

1. **Verificar Docker**: `docker --version`
2. **Verificar Make**: `make --version`  
3. **Revisar logs**: `cd proyecto_final && make docker-compose-logs`
4. **Info del sistema**: `cd proyecto_final && make info`

## Funcionalidades Destacadas

- **Interfaz Triple**: Consola, Web y API en un solo proyecto
- **Docker Ready**: Completamente containerizado
- **Make Automation**: Comandos simplificados para todo
- **UI Moderna**: Interfaz web responsive con gráficos
- **Reportes Avanzados**: Estadísticas y gráficos interactivos
- **Validación Completa**: Datos siempre consistentes
- **API Documentada**: Swagger UI automático
- **Testing**: Suite de pruebas incluida

## Autor

**Daniel Prazeres - Proyecto Final - Talento Tech**  
Sistema de Gestión de Inventario en Python con Docker y Make

---

<div align="center">

**🌟 ¡Dale una estrella si te resultó útil! 🌟**

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com)
[![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://python.org)

</div>
