# Proyecto Python Challenge

Este es un proyecto basado en **Python**, **Django**, **PostgreSQL** y **Docker**. Estos son los pasos necesarios para descargar, configurar y ejecutar el proyecto.

## Configuración del Entorno

### 1. Clonar el Repositorio

```git clone [url_del_repositorio]```
```cd python-challenge```

### 2. Configurar el Entorno Python
Chequea tener **Python 3.9** instalado. Luego, ejecuta los siguientes comandos:

```poetry env use $(which python3)```
```poetry install```

Si es necesario, ejecuta:
```poetry install --no-root```
```poetry lock --no-update```

Ejecuta:
```poetry shell```

```python manage.py makemigrations```

### 3. Configurar el Archivo .env

Crea un archivo .env en la raíz del proyecto con la siguiente información:
```DJANGO_SECRET_KEY=''
```DJANGO_DEBUG=True
```DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,172.22.0.2,172.23.0.2,172.19.0.2
```DJANGO_DB_NAME=python-challenge
```DJANGO_DB_USER=matiasmacadden
```DJANGO_DB_PASSWORD=1234
```DJANGO_DB_HOST=db
```DJANGO_DB_PORT=5432


## Configuración de Docker
### 1. Construir y Levantar Contenedores

Antes de comenzar con esta configuración, asegúrate de tener Docker instalado en tu máquina. Podes descargarlo desde [este enlace](https://www.docker.com/get-started) e instalarlo siguiendo las instrucciones proporcionadas.

Ejecuta:
```docker-compose up --build```
Este comando construirá las imágenes y levantará los contenedores de PostgreSQL y Django.

### 2. Crear Migraciones y Aplicarlas
Desde aqui, en una nueva consola.

Verifica los contenedores de Docker en ejecución:
```docker ps```
Toma el ID del contenedor de Django, cuya imagen se llama **"python-challenge-web"**.

Ejecuta el siguiente comando para ingresar al contenedor:
```docker exec -it [container_id] bash```

Navega hasta donde se encuentre el manage.py y ejecuta las migraciones:
```python manage.py migrate```

Verifica que las migraciones se hayan aplicado correctamente:
```python manage.py showmigrations```

### 3. Crear un Superusuario
```python manage.py createsuperuser```

## Ejecución del Proyecto
Ahora que todo está configurado, podés acceder al proyecto Django a través del navegador en [localhost:8000/admin/](localhost:8000/admin/) 
