# Elimina los artefactos generados por PyInstaller para el proyecto PDF-to-Image.

$folders = @(
  "build",
  "dist"
)

$files = @(
  "PDF-to-Image.spec" # Este nombre es generado por PyInstaller
)

foreach ($folder in $folders) {
  if (Test-Path -LiteralPath $folder -PathType Container) {
    Write-Host "Eliminando carpeta: $folder"
    Remove-Item -LiteralPath $folder -Recurse -Force -ErrorAction SilentlyContinue
  } else {
    Write-Host "La carpeta '$folder' no existe, no se necesita limpieza."
  }
}

foreach ($file in $files) {
  if (Test-Path -LiteralPath $file -PathType Leaf) {
    Write-Host "Eliminando archivo: $file"
    Remove-Item -LiteralPath $file -Force -ErrorAction SilentlyContinue
  } else {
    Write-Host "El archivo '$file' no existe, no se necesita limpieza."
  }
}

Write-Host "Limpieza completada."