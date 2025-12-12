import duckdb

# Conecta a la base de datos
con = duckdb.connect("delitos.db")

# Muestra tablas disponibles
print("Tablas en la base de datos:")
print(con.execute("SHOW TABLES").fetchall())

# Muestra algunas filas
print("\nPrimeras 5 filas de la tabla 'delitos':")
print(con.execute("SELECT * FROM delitos LIMIT 5").fetchdf())

# Muestra procedencias distintas
print("\nProcedencias únicas:")
print(con.execute("SELECT DISTINCT Procedencia FROM delitos").fetchall())

# Muestra tipos de delito únicos
print("\nTipos de delito únicos:")
print(con.execute("SELECT DISTINCT TipoDelito FROM delitos").fetchall())

