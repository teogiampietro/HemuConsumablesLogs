# 🧪 Extractor de Consumibles de WoW (Logs Analyzer)

Una herramienta gráfica desarrollada en Python que permite procesar logs de combate de World of Warcraft para extraer información sobre el uso de consumibles por parte de los jugadores.

## 📦 Características

- Procesa logs `.txt` y detecta líneas con uso de consumibles (`uses`).
- Limpia y agrupa datos para mostrar:
  - Qué jugador usó qué consumible.
  - Cuántas veces se usó cada uno.
- Exporta los resultados a Excel (`.xlsx`).
- Interfaz para buscar un jugador y ver cuántos consumibles usó.
- Carga de archivos `.xlsx` ya generados para consultar sin reprocesar el log.
- Reemplaza `"You gain"` por el nombre del jugador que elijas.
- Limpia consumibles tipo "Juju Power on Rivias" → conserva solo el nombre del consumible.

## 🖥️ Captura de pantalla

![image](https://github.com/user-attachments/assets/23b52928-471e-4177-a7ee-5f98500c1ee0)

## 🚀 Requisitos

- Python 3.9 o superior
- Paquetes:
  - `pandas`
  - `openpyxl`
  - `tkinter` (incluido por defecto en la mayoría de instalaciones de Python)

### Instalación de dependencias

```bash
pip install pandas openpyxl
