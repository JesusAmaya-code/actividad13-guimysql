"""Actividad 13: consulta de productos con Tkinter y MySQL."""

import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import mysql.connector
from dotenv import load_dotenv


# Buscar el archivo junto al programa, independientemente del directorio actual.
load_dotenv(Path(__file__).resolve().with_name(".env"))


def consultar_productos():
    """Devuelve los encabezados y registros sin modificar la base de datos."""
    requeridas = ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_PORT", "DB_NAME")
    faltantes = [nombre for nombre in requeridas if os.getenv(nombre) is None]
    if faltantes:
        raise ValueError("Faltan variables de configuración: " + ", ".join(faltantes))

    try:
        puerto = int(os.environ["DB_PORT"])
    except ValueError:
        raise ValueError("DB_PORT debe ser un número entero.") from None
    if not 1 <= puerto <= 65535:
        raise ValueError("DB_PORT debe estar entre 1 y 65535.")
    for nombre in ("DB_HOST", "DB_USER", "DB_NAME"):
        if not os.environ[nombre].strip():
            raise ValueError(f"{nombre} no puede estar vacío.")

    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=puerto,
            database=os.environ["DB_NAME"],
            connection_timeout=5,
        )
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        columnas = [descripcion[0] for descripcion in cursor.description]
        registros = cursor.fetchall()
        return columnas, registros
    finally:
        # El segundo finally garantiza el cierre de la conexión aunque falle
        # el cierre del cursor. También funciona si la conexión no se estableció.
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if conexion is not None:
                conexion.close()


class AplicacionProductos:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Sistema POS - Productos")
        ventana.geometry("900x520")
        ventana.minsize(600, 350)

        contenedor = ttk.Frame(ventana, padding=20)
        contenedor.pack(fill=tk.BOTH, expand=True)
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(2, weight=1)

        ttk.Label(
            contenedor, text="Consulta de productos", font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 14))

        self.boton = ttk.Button(
            contenedor, text="Mostrar productos", command=self.mostrar_productos
        )
        self.boton.grid(row=1, column=0, sticky="w", pady=(0, 14))

        marco_tabla = ttk.Frame(contenedor)
        marco_tabla.grid(row=2, column=0, sticky="nsew")
        marco_tabla.columnconfigure(0, weight=1)
        marco_tabla.rowconfigure(0, weight=1)

        self.tabla = ttk.Treeview(marco_tabla, show="headings")
        self.tabla.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(
            marco_tabla, orient=tk.VERTICAL, command=self.tabla.yview
        )
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal = ttk.Scrollbar(
            marco_tabla, orient=tk.HORIZONTAL, command=self.tabla.xview
        )
        horizontal.grid(row=1, column=0, sticky="ew")
        self.tabla.configure(
            yscrollcommand=vertical.set, xscrollcommand=horizontal.set
        )

        self.estado = tk.StringVar(value="Presiona Mostrar productos para consultar.")
        ttk.Label(contenedor, textvariable=self.estado).grid(
            row=3, column=0, sticky="w", pady=(12, 0)
        )

    def mostrar_productos(self):
        self.boton.state(["disabled"])
        self.estado.set("Consultando productos…")
        self.ventana.update_idletasks()
        try:
            columnas, registros = consultar_productos()
            # Reconstruir los encabezados en cada consulta permite cambios
            # en la estructura de la tabla sin cambiar este programa.
            self.tabla.delete(*self.tabla.get_children())
            identificadores = [f"columna_{i}" for i in range(len(columnas))]
            self.tabla.configure(columns=identificadores)
            for identificador, nombre in zip(identificadores, columnas):
                self.tabla.heading(identificador, text=nombre)
                self.tabla.column(identificador, width=160, minwidth=100, stretch=False)
            for registro in registros:
                valores = ["NULL" if valor is None else str(valor) for valor in registro]
                self.tabla.insert("", tk.END, values=valores)
            self.estado.set(f"Productos encontrados: {len(registros)}")
        except (mysql.connector.Error, ValueError) as error:
            self.estado.set("Error al consultar. Los datos anteriores no se actualizaron.")
            messagebox.showerror(
                "Error de conexión o consulta",
                f"No se pudieron consultar los productos.\n\n{error}",
                parent=self.ventana,
            )
        finally:
            self.boton.state(["!disabled"])


if __name__ == "__main__":
    raiz = tk.Tk()
    AplicacionProductos(raiz)
    raiz.mainloop()
