import json
import pandas as pd
import duckdb
import os

# Ruta al archivo JSON original
archivo_json = "datos_cruzados.json"

# Ruta para la base de datos DuckDB
archivo_db = "delitos.db"

def cargar_y_validar_json(ruta):
    """
    Intenta cargar el JSON de forma robusta, ya sea como lista o línea por línea.
    Devuelve: lista de dicts limpios o lanza error si no puede.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        texto = f.read().strip()

        # Caso 1: JSON en formato de lista
        if texto.startswith("["):
            try:
                datos = json.loads(texto)
                assert isinstance(datos, list)
                return datos
            except Exception as e:
                print("❌ Error al cargar como lista JSON:", e)

        # Caso 2: JSON línea por línea
        print("⚠️ Intentando cargar como JSON línea por línea...")
        datos = []
        with open(ruta, "r", encoding="utf-8") as f_lineas:
            for i, linea in enumerate(f_lineas, start=1):
                if linea.strip():
                    try:
                        obj = json.loads(linea)
                        datos.append(obj)
                    except json.JSONDecodeError as e:
                        print(f"❌ Línea {i} inválida: {e}")
        return datos

def convertir_a_duckdb(datos, ruta_db):
    """
    Convierte una lista de dicts a una tabla DuckDB.
    """
    df = pd.DataFrame(datos)
    print("✅ Datos cargados al DataFrame. Filas:", len(df))
    conexion = duckdb.connect(ruta_db)
    conexion.execute("CREATE OR REPLACE TABLE delitos AS SELECT * FROM df")
    print("✅ Base de datos creada:", ruta_db)
    # Mostrar 5 filas como verificación
    print(conexion.execute("SELECT * FROM delitos LIMIT 5").fetchdf())

# ---------- MAIN ----------
if __name__ == "__main__":
    if not os.path.exists(archivo_json):
        print("❌ Archivo no encontrado:", archivo_json)
    else:
        datos = cargar_y_validar_json(archivo_json)
        if datos and isinstance(datos, list):
            convertir_a_duckdb(datos, archivo_db)
        else:
            print("❌ No se pudo cargar el JSON correctamente.")
