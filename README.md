# Tienda de plantas MilesPlants - API REST

## UT3 - Integración y despliegue de aplicaciones en la nube

- **Autora:** Milena Sánchez Navarro
- **Asignatura:** Desarrollo en la Nube
- **Fecha:** 07/05/2026

## Descripción del proyecto

API REST para la gestión de una tienda de plantas. Permite el registro y autenticación de usuarios, consulta pública del catálogo y gestión privada de pedidos. El proyecto está dockerizado con MariaDB/MySQL y cuenta con un pipeline de CI/CD que automatiza la construcción, publicación en Docker Hub y despliegue en AWS EC2 mediante GitHub Actions.

## Estructura del proyecto

- **app/:** Aplicación y lógica principal
- **docker/:** Dockerfile y docker-compose.yml
- **tests/:** Pruebas automatizadas
- **.github/workflows/:** Pipeline de integración y despliegue continuo
- **.env.example:** Plantilla de variables de entorno
- **requirements.txt:** Dependencias de Python

## Instalación y configuración en local

> Deberás tener instalado Python previamente.

### 1. Clonar repositorio (o descomprimir el proyecto)

```bash
git clone <url-del-repositorio>
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv <nombre-del-entorno-virtual>
```

Activar entorno:

- Windows:

```bash
.\venv\Scripts\activate
```

- macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear fichero .env

Copia el archivo .env.example y rellena las credenciales correspondientes.

### 5. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

## Ejecución con Docker Compose

### 1. Construir las imágenes y levantar los servicios (en segundo plano)

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

### 2. Verificar que los contenedores están activos

```bash
docker compose -f docker/docker-compose.yml ps
```

### 3. Acceder a la API
> Puerto 8000 por defecto en FastAPI/Uvicorn

- http://localhost:8000
- http://localhost:8000/docs   (Documentación Swagger)
- http://localhost:8000/redoc  (Documentación ReDoc)

### 4. Detener y eliminar contenedores, redes y volúmenes

```bash
docker compose -f docker/docker-compose.yml down
```

## Despliegue

El proyecto está accesible en los siguientes enlaces:

- **Repositorio público:** https://github.com/MilesAway88/dan03-api-rest-fastapi/
- **Imagen pública en Docker Hub:** []
- **App desplegada en AWS:** []
- **Documentación generada por FastAPI:** <url-del-proyecto>/docs o <url-del-proyecto>/redoc
