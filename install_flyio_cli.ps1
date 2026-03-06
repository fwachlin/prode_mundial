# Script para instalar Fly.io CLI en Windows
# Ejecutar en PowerShell como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalación de Fly.io CLI para Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si ya está instalado
$flyPath = Get-Command fly -ErrorAction SilentlyContinue

if ($flyPath) {
    Write-Host "✓ Fly.io CLI ya está instalado" -ForegroundColor Green
    Write-Host ""
    Write-Host "Versión actual:" -ForegroundColor Yellow
    fly version
    Write-Host ""
    
    $update = Read-Host "¿Deseas actualizar a la última versión? (s/n)"
    if ($update -ne "s") {
        Write-Host "Instalación cancelada." -ForegroundColor Yellow
        exit
    }
}

Write-Host "Descargando e instalando Fly.io CLI..." -ForegroundColor Yellow
Write-Host ""

try {
    iwr https://fly.io/install.ps1 -useb | iex
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Instalación completada" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
    Write-Host "   Cierra y vuelve a abrir PowerShell para usar 'fly'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Siguiente paso:" -ForegroundColor Cyan
    Write-Host "   1. Abre una nueva ventana de PowerShell" -ForegroundColor White
    Write-Host "   2. Ejecuta: fly auth login" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ Error durante la instalación:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Instalación manual:" -ForegroundColor Yellow
    Write-Host "   Visita: https://fly.io/docs/hands-on/install-flyctl/" -ForegroundColor White
}

Write-Host ""
Write-Host "Presiona ENTER para salir..."
Read-Host
