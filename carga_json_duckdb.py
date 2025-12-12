import json
import pandas as pd
import duckdb

ruta_json = "datos_cruzados.json"

# Leer cada línea como un JSON separado
with open(ruta_json, "r", encoding="utf-8") as f:
    datos = [json.loads(line) for line in f if line.strip()]

# Convertir a DataFrame
df = pd.DataFrame(datos)

# Guardar en DuckDB
conexion = duckdb.connect("delitos.db")
conexion.execute("CREATE OR REPLACE TABLE delitos AS SELECT * FROM df")

print(conexion.execute("SELECT * FROM delitos LIMIT 5").fetchdf())
