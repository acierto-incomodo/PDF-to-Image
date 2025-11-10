#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Ejecutar el script principal
python3 main.py

# Esperar 3 segundos
sleep 3

# Cuenta regresiva de 5 a 1
echo "Cerrando en:"
for i in {5..1}
do
    echo "$i..."
    sleep 1
done

# Forzar cierre de la terminal
echo "Cerrando terminal."
kill -9 $PPID
exit
