# Iniciar Proyecto con Entorno Virtual y Django

Este archivo README.md proporciona instrucciones sobre cómo configurar y ejecutar tu proyecto utilizando un entorno virtual con Django y Python.

## Pasos

1. **Descargar el Repositorio**

    Clona o descarga el repositorio en la ubicación de tu elección.

2. **Instalar virtualenv (si no está instalado)**

    Si no tienes `virtualenv` instalado, puedes hacerlo usando el siguiente comando:

    ```bash
    pip install virtualenv
    ```

3. **Crear un entorno virtual**

    Navega a la ubicación donde descargaste el repositorio y crea un entorno virtual llamado `ENV` con el siguiente comando:

    ```bash
    virtualenv ENV
    ```

4. **Activar el entorno virtual**

    Activa el entorno virtual con el siguiente comando, dependiendo del sistema operativo:

    - **En Windows:**

        ```bash
        ENV\Scripts\activate
        ```

    - **En macOS y Linux:**

        ```bash
        source ENV/bin/activate
        ```

5. **Instalar dependencias**

    Dentro del entorno virtual, instala las dependencias Django y Python con el siguiente comando:

    ```bash
    pip install django
    ```

6. **Ejecutar el proyecto**

    Con todas las dependencias instaladas, puedes ejecutar tu proyecto Django usando el siguiente comando:

    ```bash
    python manage.py runserver
    ```

    Tu proyecto debería estar en funcionamiento en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

7. **Recrear Migraciones y Crear Superusuario**

    Una vez iniciado el proyecto, puedes realizar los siguientes pasos:

    - Borrar las migraciones existentes y la base de datos (esto eliminará todos los datos actuales):

        ```bash
        rm -Force db.sqlite3
        ```

    - Crear nuevas migraciones:

        ```bash
        python manage.py makemigrations
        ```

    - Aplicar las migraciones:

        ```bash
        python manage.py migrate
        ```

    - Crear un superusuario para acceder al panel de administración:

        ```bash
        python manage.py createsuperuser
        ```

## Más Información

Si deseas obtener más información sobre el proyecto y conocer los detalles, puedes acceder a la [página de Notion](https://www.notion.so/DJANGO_TEST-f46dc80c026445e3acda652d1fcbbf8b?pvs=4).

## Desactivar el entorno virtual

Cuando hayas terminado de trabajar en tu proyecto, puedes desactivar el entorno virtual utilizando el siguiente comando:

```bash
ENV/Scripts/deactivate
```

## Puntos no terminados
```1.- Añade pruebas unitarias para verificar el funcionamiento correcto de las vistas y modelos```
```2.- Falto pulir unos detalles en CSS```