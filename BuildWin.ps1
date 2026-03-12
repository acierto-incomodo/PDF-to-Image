# BuildWin.ps1
# Construye el proyecto PDF-to-Image en un solo ejecutable para Windows.

# 1. Limpia los artefactos de compilaciones anteriores
Write-Host "Limpiando compilaciones anteriores..."
.\Clear.ps1

# 2. Construye el ejecutable usando PyInstaller
Write-Host "Construyendo el ejecutable con PyInstaller..."
python -m PyInstaller --onefile --name "PDF-to-Image" main.py

# 3. Mensaje final
Write-Host "Proceso de compilación completado. El ejecutable se encuentra en la carpeta 'dist'."