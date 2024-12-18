import tkinter as tk
from tkinter import messagebox
import sqlite3

def crear_conexion():
    try:
        conexion = sqlite3.connect("src/database/perifericos.db")
        return conexion
    except Exception as ex:
        print(f"Error al conectar: {ex}")
        return None

def mostrar_perifericos():
    conexion = crear_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM perifericos")
        registros = cursor.fetchall()
        lista.delete(0, tk.END)  # Limpiar la lista
        for registro in registros:
            lista.insert(tk.END, f"ID: {registro[0]} | {registro[1]} | Stock: {registro[4]}")
        conexion.close()
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")

def agregar_periferico():
    nombre = entry_nombre.get()
    tipo = entry_tipo.get()
    precio = entry_precio.get()
    stock = entry_stock.get()
    if nombre and tipo and precio and stock:
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO perifericos (nombre, tipo, precio, stock) VALUES (?, ?, ?, ?)",
                           (nombre, tipo, float(precio), int(stock)))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Periférico agregado correctamente")
            mostrar_perifericos()
    else:
        messagebox.showwarning("Advertencia", "Completa todos los campos")

def eliminar_periferico():
    id_periferico = entry_id.get()
    if id_periferico:
        conexion = crear_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM perifericos WHERE id = ?", (id_periferico,))
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Éxito", "Periférico eliminado correctamente")
            mostrar_perifericos()
    else:
        messagebox.showwarning("Advertencia", "Introduce el ID del periférico a eliminar")

def reporte_bajo_stock():
    conexion = crear_conexion()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM perifericos WHERE stock <= 2")
        registros = cursor.fetchall()
        lista.delete(0, tk.END)  # Limpiar la lista
        if registros:
            for registro in registros:
                lista.insert(tk.END, f"ID: {registro[0]} | {registro[1]} | Stock: {registro[4]}")
        else:
            messagebox.showinfo("Información", "No hay productos con bajo stock")
        conexion.close()
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")

root = tk.Tk()
root.title("Gestión de Periféricos")
root.geometry("600x600")

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Nombre:").grid(row=0, column=0)
entry_nombre = tk.Entry(frame_form)
entry_nombre.grid(row=0, column=1, padx=5)

tk.Label(frame_form, text="Tipo:").grid(row=1, column=0)
entry_tipo = tk.Entry(frame_form)
entry_tipo.grid(row=1, column=1, padx=5)

tk.Label(frame_form, text="Precio:").grid(row=2, column=0)
entry_precio = tk.Entry(frame_form)
entry_precio.grid(row=2, column=1, padx=5)

tk.Label(frame_form, text="Stock:").grid(row=3, column=0)
entry_stock = tk.Entry(frame_form)
entry_stock.grid(row=3, column=1, padx=5)

tk.Label(frame_form, text="ID:").grid(row=4, column=0)
entry_id = tk.Entry(frame_form)
entry_id.grid(row=4, column=1, padx=5)

# Botones
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_agregar = tk.Button(frame_buttons, text="Agregar Periférico", command=agregar_periferico)
btn_agregar.grid(row=0, column=0, padx=5)

btn_mostrar = tk.Button(frame_buttons, text="Mostrar Periféricos", command=mostrar_perifericos)
btn_mostrar.grid(row=0, column=1, padx=5)

btn_eliminar = tk.Button(frame_buttons, text="Eliminar Periférico", command=eliminar_periferico)
btn_eliminar.grid(row=0, column=2, padx=5)

btn_bajo_stock = tk.Button(frame_buttons, text="Reporte Bajo Stock", command=reporte_bajo_stock)
btn_bajo_stock.grid(row=0, column=3, padx=5)

# Listbox para mostrar los resultados
lista = tk.Listbox(root, width=80, height=20)
lista.pack(pady=10)

# Iniciar la aplicación
root.mainloop()
