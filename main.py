import sys
import subprocess
import json
from config import menu  # Usa tu ventana de configuración

def launch_screensaver():
    """Ejecuta RPS.py o RPS_BigBangTheory.py según la config"""
    try:
        with open('config.json') as f:
            config = json.load(f)
        mode = config.get('mode', 'Classic')
    except Exception:
        mode = 'Classic'

    if mode == 'Classic':
        subprocess.run(["python", "RPS.py"])
    elif mode == 'Big Bang Theory':
        subprocess.run(["python", "RPS_BigBangTheory.py"])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg.startswith("/c"):  # Modo configuración
            menu()
        elif arg.startswith("/s"):  # Modo protector
            launch_screensaver()
        elif arg.startswith("/p"):  # Vista previa (ignorada)
            pass
    else:
        launch_screensaver()
