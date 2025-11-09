#!/bin/bash
# Build script para Render - Instala ODBC Driver y dependencias Python

set -o errexit  # Exit on error

echo "==> Installing ODBC Driver 18 for SQL Server..."

# Instalar dependencias del sistema
apt-get update
apt-get install -y curl gnupg2

# Agregar repositorio de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Actualizar e instalar ODBC Driver
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

echo "==> ODBC Driver installed successfully!"

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Build completed!"
