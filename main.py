# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import duckdb
from interpretador import generar_sql  # Usa tu lógica actual
from openai_client import obtener_respuesta_gpt
from init_db import init_db, registrar_consulta

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

 # Crear tabla cuando arranca app
init_db()

# Rutas para frontend
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

@app.get("/")
def get_frontend():
    return FileResponse("frontend.html")


DB_PATH_DATOS = "delitos.db"  # Asegúrate de que apunte al archivo correcto
DB_PATH_CONSULTAS = "consultas.db" #DB  de  consultas para registro

class Consulta(BaseModel):
    frase: str


@app.post("/responder")
def responder(consulta: Consulta):
    sql_por_procedencia, sql_total_general = generar_sql(consulta.frase)

    if sql_por_procedencia.startswith("-- NO_DETECTADO"):
        return {
            "frase": consulta.frase,
            "sql": sql_por_procedencia,
            "resultado": None,
            "mensaje": (
                "Soy una inteligencia artificial diseñada para ayudarte a consultar datos "
                "sobre tipos de delitos y procedencias en España, basados en estadísticas oficiales. "
                "Puedes preguntar, por ejemplo: '¿Cuántos hurtos cometieron los europeos?' "
                "o simplemente '¿Cuántos homicidios hubo?'."
            )
        }

    try:
        conn = duckdb.connect(database=DB_PATH_DATOS, read_only=True)
        cursor = conn.cursor()
        cursor.execute(sql_por_procedencia)
        rows = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(columnas, row)) for row in rows]

        # ❗️Filtrar resultados para excluir la procedencia "Total"
        resultados_filtrados = [r for r in resultados if r["Procedencia"] != "Total"]

        # Generar tabla procedencia
        datos_texto = "Procedencia, TipoDelito, Total\n"
        datos_texto += "\n".join(
            f"{r['Procedencia']}, {r['TipoDelito']}, {int(r['Total'])}" for r in resultados_filtrados
        )
        
        # Ejecutar consulta total general
        cursor.execute(sql_total_general)
        rows_total = cursor.fetchall()
        columnas_total = [desc[0] for desc in cursor.description]
        resultados_total = [dict(zip(columnas_total, row)) for row in rows_total]

        # Generar tabla de texto total general
        datos_total_texto = "TipoDelito, Total\n"
        datos_total_texto += "\n".join(
            f"{r['TipoDelito']}, {int(r['Total'])}" for r in resultados_total
        )

        conn.close()

        # Crear prompt para GPT
        prompt = (
            "Eres un asistente que responde dudas o percepciones sobre delitos en España con datos oficiales del Instituto Nacional de Estadística (INE) de 2023.\n\n"
            f"El usuario ha escrito: \"{consulta.frase}\"\n\n"
            "A continuación, el sistema ha recuperado datos oficiales del Instituto Nacional de Estadística (INE) de 2023 relacionados con esa frase. El usuario no ha proporcionado estos datos: los aporta el sistema para ayudarte a dar una respuesta fundamentada:\n\n"
            f"{datos_texto}\n\n"
            "Y los datos totales sin filtrar (todas las procedencias combinadas):\n\n"
            f"{datos_total_texto}\n\n"
            "Usa estos datos para responder de forma clara y objetiva, sin hacer juicios morales ni discursos ideológicos. "
            "Limítate a explicar lo que muestran los datos y señala con respeto si alguna expresión puede resultar ofensiva o discriminatoria, explicando por qué. "
            "El objetivo es que el usuario entienda mejor los datos y saque sus propias conclusiones."
            "Cuando sea posible, calcula y menciona los porcentajes relativos de los delitos cometidos por cada grupo respecto al total."
        )

        # Llama a OpenAi
        respuesta_gpt = obtener_respuesta_gpt(prompt)

        # Registra Consulta
        registrar_consulta(consulta.frase, sql_por_procedencia, sql_total_general)

        return {
            "frase": consulta.frase,
            "sql": sql_por_procedencia,
            "sql_total_general": sql_total_general,
            "resultado": resultados_filtrados,
            "resultado_total_general": resultados_total,
            "prompt_para_openai": prompt,
            "respuesta_gpt": respuesta_gpt,
        }

    except Exception as e:
        return {"error": str(e)}
