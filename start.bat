@echo off
REM Activar el entorno virtual
call venv\Scripts\activate

REM Ejecutar el script principal
python main.py

REM Esperar 3 segundos
echo Esperando 3 segundos...
timeout /t 3 >nul

REM Cuenta regresiva de 5 a 1
echo Cerrando en:
for /l %%i in (5,-1,1) do (
    echo %%i...
    timeout /t 1 >nul
)

REM Forzar cierre de la consola
echo Cerrando terminal...
taskkill /f /im cmd.exe >nul 2>&1
exit
