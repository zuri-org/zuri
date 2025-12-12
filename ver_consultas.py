import duckdb

conn = duckdb.connect('consultas.db')
cursor = conn.cursor()

# Ver tabla
print("Tablas existentes:")
cursor.execute("SHOW TABLES")
print(cursor.fetchall())

# Ver filas
cursor.execute("SELECT * FROM consultas")
registros = cursor.fetchall()

print("\nConsultas registradas:")
for fila in registros:
    print(fila)

conn.close()
