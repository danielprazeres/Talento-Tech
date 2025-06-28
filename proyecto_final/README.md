# Sistema de Gestión de Inventario

> **Ver documentación completa en [README principal](../README.md)**

## Inicio Rápido

```bash
# Levantar todos los servicios con Docker
make quick-start

# O ejecutar interfaz web local
make run-web
```

## Comandos Principales

```bash
# Ver todos los comandos disponibles
make help

# Desarrollo local
make run-web          # Interfaz web (puerto 8501)
make run-api          # API REST (puerto 8000)  
make run-console      # Interfaz de consola
make test             # Ejecutar pruebas

# Docker Compose
make quick-start      # Iniciar servicios
make quick-stop       # Detener servicios
make docker-compose-logs  # Ver logs
```

## URLs de Acceso

- **Interfaz Web**: http://localhost:8501
- **API REST**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Archivos Principales

- `main.py` - Interfaz de consola
- `app_streamlit.py` - Interfaz web
- `api.py` - API REST
- `database.py` - Manejo de base de datos
- `inventario.py` - Lógica de negocio
- `Dockerfile` - Configuración Docker
- `docker-compose.yml` - Orquestación de servicios
- `Makefile` - Comandos automatizados

---

**Para documentación completa, ejemplos detallados y capturas de pantalla, ver el [README principal](../README.md)** 