@echo off
REM Crear entorno virtual si no existe
if not exist venv (
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate

REM (Opcional) Instalar dependencias automáticamente
if exist requirements.txt (
    echo 🔹 Instalando dependencias...
    pip install -r requirements.txt
)

echo ✅ Entorno activado. Python en uso:
where python

echo Iniciando PDF to Image:
for /l %%i in (3,-1,1) do (
    echo %%i...
    timeout /t 1 >nul
)

REM Ejecutar el siguiente script (start.sh o su equivalente .bat)
call start.bat

REM Si en realidad quieres ejecutar el .sh desde Windows (usando Git Bash o similar):
REM bash start.sh
