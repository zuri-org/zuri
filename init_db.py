import duckdb
import os

# Ruta del archivo donde se almacenarán los registros de consultas
DB_PATH_CONSULTAS = os.path.join(os.getcwd(), "consultas.db")

def init_db():
    conn = duckdb.connect(DB_PATH_CONSULTAS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id BIGINT,
            frase VARCHAR,
            sql VARCHAR,
            sql_total_general VARCHAR,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def registrar_consulta(frase, sql, sql_total_general):
    conn = duckdb.connect(DB_PATH_CONSULTAS)
    cursor = conn.cursor()
    # Último id
    cursor.execute("SELECT MAX(id) FROM consultas")
    max_id = cursor.fetchone()[0]
    if max_id is None: 
        max_id = 0 
    nuevo_id = max_id + 1

    cursor.execute(
        "INSERT INTO consultas (id, frase, sql, sql_total_general) VALUES (?, ?, ?, ?)",
        (nuevo_id, frase, sql, sql_total_general)
    )
    conn.commit()
    conn.close()
