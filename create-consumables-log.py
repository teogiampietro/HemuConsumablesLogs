import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re

pivot_data = None  # Variable global para guardar la tabla procesada

def cargar_excel():
    global pivot_data
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", ".xlsx")])
    if not filepath:
        return
    try:
        df = pd.read_excel(filepath, index_col=0)
        pivot_data = df
        messagebox.showinfo("Éxito", f"Archivo cargado correctamente.\nAhora podés buscar por jugador.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")


def procesar_log():
    global pivot_data
    personaje = entry_personaje.get().strip().lower()
    if not personaje:
        messagebox.showwarning("Campo requerido", "Por favor, ingrese el nombre del personaje.")
        return

    filepath = filedialog.askopenfilename(filetypes=[("Text files", ".txt")])
    if not filepath:
        return

    data = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = re.sub(r"\bYou gain\b", f"{personaje} gains", line, flags=re.IGNORECASE)

            if "uses" in line.lower():
                match = re.search(r"\s*(\w+)\s+uses\s+(.+)", line, re.IGNORECASE)
                if match:
                    jugador = match.group(1)
                    consumible = match.group(2).strip().rstrip(".")
                    consumible = re.sub(r"\s+on\s+.*$", "", consumible, flags=re.IGNORECASE)
                    data.append((jugador.lower(), consumible))

    if not data:
        messagebox.showinfo("Resultado", "No se encontraron líneas con 'uses'.")
        return

    df = pd.DataFrame(data, columns=["Jugador", "Consumible"])
    pivot = df.pivot_table(index="Consumible", columns="Jugador", aggfunc="size", fill_value=0)
    pivot_data = pivot 

    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", ".xlsx")])
    if save_path:
        pivot.to_excel(save_path)
        messagebox.showinfo("Éxito", f"Resumen guardado en: {save_path}")

def mostrar_consumibles():
    global pivot_data
    nombre = entry_busqueda.get().strip().lower()
    if pivot_data is None:
        messagebox.showwarning("Primero procesá el log", "Tenés que procesar un log antes de buscar.")
        return

    if nombre not in pivot_data.columns:
        messagebox.showinfo("No encontrado", f"No se encontraron datos para el jugador: {nombre}")
        return

    resultados = pivot_data[nombre]
    text_resultado.config(state="normal")
    text_resultado.delete(1.0, tk.END)
    for consumible, cantidad in resultados.items():
        if cantidad > 0:
            text_resultado.insert(tk.END, f"{consumible}: {cantidad}\n")
    text_resultado.config(state="disabled")

# Interfaz
root = tk.Tk()
root.title("Resumen de Consumibles por Jugador")

frame_input = tk.Frame(root)
frame_input.pack(padx=20, pady=10)

tk.Label(frame_input, text="Nombre para reemplazar 'You gain':").grid(row=0, column=0, sticky="e")
entry_personaje = tk.Entry(frame_input, width=30)
entry_personaje.grid(row=0, column=1, padx=10)

btn_procesar = tk.Button(root, text="Seleccionar Log y Generar Resumen", command=procesar_log, height=2, width=35)
btn_procesar.pack(pady=10)

btn_cargar_excel = tk.Button(root, text="Cargar archivo .xlsx existente", command=cargar_excel, height=2, width=35)
btn_cargar_excel.pack(pady=5)

separator = tk.Frame(height=2, bd=1, relief="sunken")
separator.pack(fill="x", padx=10, pady=10)

frame_busqueda = tk.Frame(root)
frame_busqueda.pack(padx=20, pady=10)

tk.Label(frame_busqueda, text="Buscar consumibles por jugador:").grid(row=0, column=0, sticky="e")
entry_busqueda = tk.Entry(frame_busqueda, width=30)
entry_busqueda.grid(row=0, column=1, padx=10)

btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=mostrar_consumibles)
btn_buscar.grid(row=0, column=2, padx=10)

text_resultado = tk.Text(root, height=30, width=60, state="disabled")
text_resultado.pack(pady=10)

root.mainloop()
