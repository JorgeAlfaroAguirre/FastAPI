#!/bin/bash
# Build script para Render - Instala ODBC Driver y dependencias Python

set -o errexit  # Exit on error

echo "=========================================="
echo "==> STARTING BUILD PROCESS"
echo "=========================================="

echo ""
echo "==> Step 1: Installing system dependencies..."
apt-get update -qq
apt-get install -y curl gnupg2
echo "✓ System dependencies installed"

echo ""
echo "==> Step 2: Adding Microsoft repository..."
curl -s https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl -s https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
echo "✓ Microsoft repository added"

echo ""
echo "==> Step 3: Installing ODBC Driver 18 for SQL Server..."
apt-get update -qq
ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev
echo "✓ ODBC Driver 18 installed"

echo ""
echo "==> Step 4: Verifying ODBC Driver installation..."
odbcinst -q -d -n "ODBC Driver 18 for SQL Server" || echo "⚠ Driver verification failed"
echo ""

echo "==> Step 5: Listing installed ODBC drivers..."
odbcinst -q -d
echo ""

echo "==> Step 6: Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Python dependencies installed"

echo ""
echo "=========================================="
echo "==> BUILD COMPLETED SUCCESSFULLY!"
echo "=========================================="
echo ""
echo "Installed components:"
echo "  - ODBC Driver 18 for SQL Server"
echo "  - unixODBC development libraries"
echo "  - Python packages from requirements.txt"
echo ""
