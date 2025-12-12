import os
from openai import OpenAI
from dotenv import load_dotenv

# Carga variables del archivo .env
load_dotenv()

# Configura la API Key
client = OpenAI()

def obtener_respuesta_gpt(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente que combate prejuicios hacia personas migrantes usando datos oficiales del INE (España, 2023)."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.5,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error al obtener respuesta de OpenAI: \n\n{str(e)}"
