# Makefile para Sistema de Gestión de Inventario
# ===============================================

.PHONY: help install run-console run-web run-api test clean docker-build docker-run-api docker-run-web docker-run-console docker-test docker-stop docker-clean docker-compose-up docker-compose-down docker-compose-logs

# Variables
PYTHON = python3
PIP = pip3
VENV = venv
DOCKER_IMAGE = inventario-sistema
DOCKER_TAG = latest

# Configuración por defecto
.DEFAULT_GOAL := help

# Ayuda - muestra todos los comandos disponibles
help: ## 📋 Mostrar esta ayuda
	@echo "🎯 Sistema de Gestión de Inventario - Comandos Disponibles"
	@echo "=========================================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "📦 Para empezar rápido: make install && make run-web"

# Configuración del entorno local
install: ## 📥 Instalar dependencias en entorno virtual
	@echo "📥 Instalando dependencias..."
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/$(PIP) install --upgrade pip
	$(VENV)/bin/$(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas en $(VENV)/"

install-global: ## 🌐 Instalar dependencias globalmente
	@echo "📥 Instalando dependencias globalmente..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas globalmente"

# Ejecución local (sin Docker)
run-console: ## 💻 Ejecutar interfaz de consola
	@echo "💻 Iniciando interfaz de consola..."
	$(PYTHON) main.py

run-web: ## 🌐 Ejecutar interfaz web (Streamlit) en puerto 8501
	@echo "🌐 Iniciando interfaz web..."
	@echo "📍 URL: http://localhost:8501"
	streamlit run app_streamlit.py

run-api: ## 🚀 Ejecutar API REST en puerto 8000
	@echo "🚀 Iniciando API REST..."
	@echo "📍 URL: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/docs"
	$(PYTHON) api.py

test: ## 🧪 Ejecutar script de pruebas
	@echo "🧪 Ejecutando pruebas del sistema..."
	$(PYTHON) test_sistema.py

# Comandos de limpieza
clean: ## 🧹 Limpiar archivos temporales
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f *.db
	@echo "✅ Limpieza completada"

clean-venv: ## 🗑️ Eliminar entorno virtual
	@echo "🗑️ Eliminando entorno virtual..."
	rm -rf $(VENV)
	@echo "✅ Entorno virtual eliminado"

# Comandos de Docker
docker-build: ## 🐳 Construir imagen Docker
	@echo "🐳 Construyendo imagen Docker..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "✅ Imagen construida: $(DOCKER_IMAGE):$(DOCKER_TAG)"

docker-run-api: docker-build ## 🚀 Ejecutar API en Docker (puerto 8000)
	@echo "🚀 Ejecutando API en Docker..."
	@echo "📍 URL: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/docs"
	docker run -p 8000:8000 --name inventario-api-container $(DOCKER_IMAGE):$(DOCKER_TAG) api

docker-run-web: docker-build ## 🌐 Ejecutar Streamlit en Docker (puerto 8501)
	@echo "🌐 Ejecutando interfaz web en Docker..."
	@echo "📍 URL: http://localhost:8501"
	docker run -p 8501:8501 --name inventario-web-container $(DOCKER_IMAGE):$(DOCKER_TAG) web

docker-run-console: docker-build ## 💻 Ejecutar consola en Docker (interactivo)
	@echo "💻 Ejecutando interfaz de consola en Docker..."
	docker run -it --name inventario-console-container $(DOCKER_IMAGE):$(DOCKER_TAG) console

docker-test: docker-build ## 🧪 Ejecutar pruebas en Docker
	@echo "🧪 Ejecutando pruebas en Docker..."
	docker run --name inventario-test-container $(DOCKER_IMAGE):$(DOCKER_TAG) test

docker-stop: ## ⏹️ Detener todos los contenedores
	@echo "⏹️ Deteniendo contenedores..."
	-docker stop inventario-api-container inventario-web-container inventario-console-container inventario-test-container
	-docker rm inventario-api-container inventario-web-container inventario-console-container inventario-test-container
	@echo "✅ Contenedores detenidos"

docker-clean: docker-stop ## 🧹 Limpiar imágenes y contenedores Docker
	@echo "🧹 Limpiando recursos Docker..."
	-docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG)
	docker system prune -f
	@echo "✅ Limpieza Docker completada"

# Comandos de Docker Compose
docker-compose-up: ## 🎼 Levantar todos los servicios con Docker Compose
	@echo "🎼 Levantando servicios con Docker Compose..."
	@echo "📍 API: http://localhost:8000"
	@echo "📍 Web: http://localhost:8501"
	mkdir -p data
	docker-compose up --build

docker-compose-up-detached: ## 🎼 Levantar servicios en segundo plano
	@echo "🎼 Levantando servicios en segundo plano..."
	mkdir -p data
	docker-compose up --build -d
	@echo "✅ Servicios ejecutándose en segundo plano"
	@echo "📍 API: http://localhost:8000"
	@echo "📍 Web: http://localhost:8501"

docker-compose-down: ## ⏹️ Detener servicios de Docker Compose
	@echo "⏹️ Deteniendo servicios..."
	docker-compose down
	@echo "✅ Servicios detenidos"

docker-compose-logs: ## 📋 Ver logs de los servicios
	@echo "📋 Mostrando logs de los servicios..."
	docker-compose logs -f

docker-compose-test: ## 🧪 Ejecutar pruebas con Docker Compose
	@echo "🧪 Ejecutando pruebas con Docker Compose..."
	docker-compose --profile testing up --build inventario-test

# Comandos de desarrollo
dev-setup: install ## 🛠️ Configuración completa para desarrollo
	@echo "🛠️ Configurando entorno de desarrollo..."
	@echo "✅ Entorno listo para desarrollo"
	@echo "💡 Comandos útiles:"
	@echo "   make run-web    - Interfaz web"
	@echo "   make run-api    - API REST"
	@echo "   make test       - Ejecutar pruebas"

# Comandos de producción
prod-docker: docker-compose-up-detached ## 🚀 Desplegar en producción con Docker
	@echo "🚀 Sistema desplegado en producción"
	@echo "📍 Servicios disponibles:"
	@echo "   API: http://localhost:8000"
	@echo "   Web: http://localhost:8501"

# Información del sistema
info: ## ℹ️ Mostrar información del sistema
	@echo "ℹ️ Información del Sistema de Inventario"
	@echo "========================================"
	@echo "📁 Directorio: $(PWD)"
	@echo "🐍 Python: $(shell $(PYTHON) --version 2>&1)"
	@echo "📦 Pip: $(shell $(PIP) --version 2>&1)"
	@echo "🐳 Docker: $(shell docker --version 2>&1 || echo 'No instalado')"
	@echo "🎼 Docker Compose: $(shell docker-compose --version 2>&1 || echo 'No instalado')"
	@echo ""
	@echo "📊 Archivos del proyecto:"
	@ls -la *.py requirements.txt 2>/dev/null || echo "❌ Archivos no encontrados"

# Comandos rápidos
quick-start: docker-compose-up-detached ## ⚡ Inicio rápido (Docker Compose en segundo plano)

quick-stop: docker-compose-down ## ⚡ Parada rápida

restart: docker-compose-down docker-compose-up-detached ## 🔄 Reiniciar servicios 