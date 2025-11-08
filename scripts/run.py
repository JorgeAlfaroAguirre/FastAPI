#!/usr/bin/env python3
"""
Script de comandos para la aplicación Barista
Uso: python scripts/run.py [comando]

Comandos disponibles:
- dev: Ejecutar en modo desarrollo
- prod: Ejecutar en modo producción (local)
- render: Ejecutar para Render (con variable PORT)
- test: Ejecutar tests
- install: Instalar dependencias
"""

import sys
import subprocess
import os
import signal

def run_command(cmd, description=""):
    """Ejecutar un comando del sistema"""
    print(f">> {description}")
    print(f"Ejecutando: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True)
        return result.returncode
    except KeyboardInterrupt:
        print("\nAplicacion detenida por el usuario")
        print("Hasta luego!")
        return 0  # Salir sin error cuando se usa Ctrl+C

def main():
    if len(sys.argv) < 2:
        print("ERROR: Debes especificar un comando")
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Cambiar al directorio del proyecto
    project_root = os.path.dirname(os.path.dirname(__file__))
    os.chdir(project_root)
    
    commands = {
        'dev': {
            'cmd': 'uvicorn app.main:app --reload --host 0.0.0.0 --port 8000',
            'desc': 'Ejecutando aplicación en modo desarrollo'
        },
        'prod': {
            'cmd': 'uvicorn app.main:app --host 0.0.0.0 --port 8000',
            'desc': 'Ejecutando aplicación en modo producción (local)'
        },
        'render': {
            'cmd': f'uvicorn app.main:app --host 0.0.0.0 --port {os.getenv("PORT", "8000")}',
            'desc': 'Ejecutando aplicación para Render'
        },
        'test': {
            'cmd': 'pytest tests/ -v',
            'desc': 'Ejecutando tests'
        },
        'test-watch': {
            'cmd': 'pytest tests/ -v --tb=short -x',
            'desc': 'Ejecutando tests en modo watch'
        },
        'install': {
            'cmd': 'pip install -r requirements.txt',
            'desc': 'Instalando dependencias'
        },
        'format': {
            'cmd': 'black app/ tests/',
            'desc': 'Formateando código'
        },
        'lint': {
            'cmd': 'flake8 app/ tests/',
            'desc': 'Ejecutando linting'
        }
    }
    
    if command not in commands:
        print(f"ERROR: Comando '{command}' no reconocido")
        print("\nComandos disponibles:")
        for cmd, info in commands.items():
            print(f"  {cmd}: {info['desc']}")
        sys.exit(1)
    
    # Ejecutar el comando
    cmd_info = commands[command]
    return run_command(cmd_info['cmd'], cmd_info['desc'])

if __name__ == "__main__":
    sys.exit(main())