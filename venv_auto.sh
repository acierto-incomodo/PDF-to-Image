#!/bin/bash

# Nombre del entorno virtual
VENV_DIR="venv"

# Comprobamos si existe el entorno virtual
if [ ! -d "$VENV_DIR" ]; then
    echo "🔹 Creando entorno virtual de Python..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Entorno virtual creado en ./$VENV_DIR"
else
    echo "✅ Entorno virtual ya existe."
fi

# Activamos el entorno virtual
echo "🔹 Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# (Opcional) Instalar dependencias automáticamente
if [ -f "requirements.txt" ]; then
    echo "🔹 Instalando dependencias..."
    pip install -r requirements.txt
fi

echo "✅ Entorno activado. Python en uso:"
which python
