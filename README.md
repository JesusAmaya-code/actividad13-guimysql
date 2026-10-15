# Actividad 13: Python y MySQL en GUI

Aplicación de escritorio con Tkinter para consultar una tabla `productos` existente en MySQL o MariaDB. Ejecuta únicamente `SELECT * FROM productos`; no crea bases de datos ni modifica registros o tablas.

## 1. Preparar Python

Se recomienda Python 3.10 o superior con Tkinter instalado. En la terminal de VS Code, abre la carpeta del proyecto y ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell impide activar el entorno, puedes instalar y ejecutar directamente con su intérprete:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe guimysql.py
```

Tkinter forma parte de la instalación habitual de Python en Windows y no se instala con pip. Puedes comprobar su disponibilidad con `python -m tkinter`. En Linux, puede ser necesario instalar el paquete `python3-tk` del sistema.

## 2. Configurar la conexión

Copia la plantilla en la terminal de PowerShell:

```powershell
Copy-Item .env.example .env
```

Edita `.env` con los datos reales del servidor y el nombre de la base de datos existente. Configura `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_PORT` y `DB_NAME`. Si una contraseña contiene `#` o espacios, colócala entre comillas. Una contraseña vacía se expresa como `DB_PASSWORD=` si tu servidor permite ese acceso.

El servidor MySQL o MariaDB debe estar iniciado y el usuario debe tener permiso de lectura sobre `productos`. No se necesita permiso de escritura. El archivo `.env` se carga desde la carpeta de `guimysql.py`; las variables ya definidas en el entorno tienen prioridad. No compartas el archivo `.env`: está excluido de Git.

## 3. Ejecutar

Con el entorno virtual activo:

```powershell
python guimysql.py
```

La ventana se titula **Sistema POS - Productos**. Pulsa **Mostrar productos** para cargar o actualizar los registros. Los encabezados se obtienen automáticamente de `cursor.description`, sin asumir nombres ni cantidad de columnas. La tabla incluye desplazamiento vertical y horizontal y muestra `NULL` para valores SQL nulos.

## 4. Probar la aplicación

- Con datos válidos, pulsa **Mostrar productos** y compara los encabezados, registros y cantidad con `SELECT * FROM productos` en tu cliente habitual de MySQL.
- Pulsa nuevamente el botón: los registros se reemplazan, sin duplicarse.
- Si la tabla está vacía, se muestran los encabezados y `Productos encontrados: 0`.
- Para comprobar el mensaje de error, configura temporalmente un `DB_PORT` incorrecto en `.env`, reinicia la aplicación y pulsa el botón. Restaura después el valor correcto. No es necesario modificar ninguna tabla.
- Si el usuario no tiene permisos o la tabla no existe en la base configurada, se muestra el error de MySQL. Revisa `DB_NAME` y los permisos con el administrador.

El cursor y la conexión se cierran después de cada consulta, incluso cuando ocurre un error. Para mantener el código sencillo, la consulta se ejecuta en el hilo de la interfaz: la ventana puede dejar de responder mientras el servidor responde. La aplicación carga todos los registros y está pensada para una tabla de tamaño adecuado para esta tarea universitaria.
