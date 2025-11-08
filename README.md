# BaristaApp

Aplicación FastAPI para gestión de barista.

## Requisitos previos

- Python 3.8 o superior
- pip

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd BaristaApp
```

2. Crear y activar el entorno virtual:

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Levantar el sistema

El proyecto incluye un script de comandos para facilitar la ejecución. Usa:

### Modo desarrollo (con hot-reload)
```bash
python scripts/run.py dev
```

El servidor estará disponible en: **http://localhost:8000** o **http://127.0.0.1:8000**

### Modo producción (local)
```bash
python scripts/run.py prod
```

### Otros comandos disponibles

- **Ejecutar tests:**
  ```bash
  python scripts/run.py test
  ```

- **Ejecutar tests en modo watch:**
  ```bash
  python scripts/run.py test-watch
  ```

- **Instalar dependencias:**
  ```bash
  python scripts/run.py install
  ```

- **Formatear código:**
  ```bash
  python scripts/run.py format
  ```

- **Ejecutar linting:**
  ```bash
  python scripts/run.py lint
  ```

### Comando directo con uvicorn

Si prefieres ejecutar directamente con uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentación API

Una vez levantado el sistema, puedes acceder a:

- **Documentación interactiva (Swagger UI):** http://localhost:8000/docs
- **Documentación alternativa (ReDoc):** http://localhost:8000/redoc

## Endpoints disponibles

- `GET /` - Health check y listado de rutas disponibles (http://localhost:8000)
- `GET /miapp` - Endpoint principal (http://localhost:8000/miapp)
