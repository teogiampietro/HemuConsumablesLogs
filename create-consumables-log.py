import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re

def procesar_log():
    personaje = entry_personaje.get().strip()
    if not personaje:
        messagebox.showwarning("Campo requerido", "Por favor, ingrese el nombre del personaje.")
        return

    filepath = filedialog.askopenfilename(filetypes=[("Text files", ".txt")])
    if not filepath:
        return

    data = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            # Reemplazar "You gain" por "<personaje> gains"
            line = re.sub(r"\bYou gain\b", f"{personaje} gains", line, flags=re.IGNORECASE)

            if "uses" in line.lower():
                match = re.search(r"\s*(\w+)\s+uses\s+(.+)", line, re.IGNORECASE)
                if match:
                    jugador = match.group(1)
                    consumible = match.group(2).strip().rstrip(".")
                    data.append((jugador, consumible))

    if not data:
        messagebox.showinfo("Resultado", "No se encontraron líneas con 'uses'.")
        return

    df = pd.DataFrame(data, columns=["Jugador", "Consumible"])
    pivot = df.pivot_table(index="Jugador", columns="Consumible", aggfunc="size", fill_value=0)

    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", ".xlsx")])
    if save_path:
        pivot.to_excel(save_path)
        messagebox.showinfo("Éxito", f"Resumen guardado en: {save_path}")

# Interfaz gráfica
root = tk.Tk()
root.title("Resumen de Consumibles por Jugador")

frame = tk.Frame(root)
frame.pack(padx=20, pady=10)

lbl = tk.Label(frame, text="Nombre del personaje para reemplazar 'You gain':")
lbl.grid(row=0, column=0, sticky="e")

entry_personaje = tk.Entry(frame, width=30)
entry_personaje.grid(row=0, column=1, padx=10)

btn = tk.Button(root, text="Seleccionar Log y Generar Resumen", command=procesar_log, height=2, width=35)
btn.pack(pady=20)

root.mainloop()
