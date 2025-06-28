FROM python:3.10-slim

# Configurar el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Crear directorio para la base de datos
RUN mkdir -p /app/data

# Exponer puertos para las diferentes interfaces
EXPOSE 8000 8501

# Crear script de entrada que permita ejecutar diferentes servicios
RUN echo '#!/bin/bash\n\
case "$1" in\n\
  "api")\n\
    echo "🚀 Iniciando API (FastAPI)..."\n\
    python api.py\n\
    ;;\n\
  "web")\n\
    echo "🌐 Iniciando interfaz web (Streamlit)..."\n\
    streamlit run app_streamlit.py --server.address 0.0.0.0 --server.port 8501\n\
    ;;\n\
  "console")\n\
    echo "💻 Iniciando interfaz de consola..."\n\
    python main.py\n\
    ;;\n\
  "test")\n\
    echo "🧪 Ejecutando pruebas del sistema..."\n\
    python test_sistema.py\n\
    ;;\n\
  *)\n\
    echo "❌ Uso: docker run <imagen> [api|web|console|test]"\n\
    echo ""\n\
    echo "Opciones disponibles:"\n\
    echo "  api      - Ejecutar API REST (puerto 8000)"\n\
    echo "  web      - Ejecutar interfaz web Streamlit (puerto 8501)"\n\
    echo "  console  - Ejecutar interfaz de consola"\n\
    echo "  test     - Ejecutar script de pruebas"\n\
    exit 1\n\
    ;;\n\
esac' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Establecer el punto de entrada
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["api"] 