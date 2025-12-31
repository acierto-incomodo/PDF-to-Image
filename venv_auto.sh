#!/bin/bash

python3 -m venv venv

source venv/bin/activate

# (Opcional) Instalar dependencias automáticamente
if [ -f "requirements.txt" ]; then
    echo "🔹 Instalando dependencias..."
    pip install -r requirements.txt
fi

echo "✅ Entorno activado. Python en uso:"
which python

echo "Iniciando PDF to Image:"
for i in {3..1}
do
    echo "$i..."
    sleep 1
done
./start.sh
