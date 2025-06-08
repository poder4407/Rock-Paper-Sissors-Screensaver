import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONFIG_PATH = "config.json"

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

def menu():
    root = tk.Tk()
    root.title("RPS Screensaver Configuration")

    config = load_config()

    # Valores por defecto
    default_config = {
        "mode": "Classic"
    }
    config = {**default_config, **config}

    # Etiqueta y combo de modo
    ttk.Label(root, text="Game Mode:").grid(row=0, column=0, padx=40, pady=40)
    mode_var = tk.StringVar(value=config["mode"])
    mode_combo = ttk.Combobox(root, textvariable=mode_var, state="readonly")
    mode_combo['values'] = ("Classic", "Big Bang Theory")
    mode_combo.grid(row=0, column=1, padx=20, pady=20)

    # Botones
    def on_save():
        config["mode"] = mode_var.get()
        save_config(config)
        messagebox.showinfo("Guardado", "Configuración guardada.")
        root.destroy()

    def on_cancel():
        root.destroy()

    ttk.Button(root, text="Guardar", command=on_save).grid(row=1, column=0, padx=20, pady=20)
    ttk.Button(root, text="Cancelar", command=on_cancel).grid(row=1, column=1, padx=20, pady=20)


    root.mainloop()
