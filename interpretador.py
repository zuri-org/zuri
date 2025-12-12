from semantica import detectar_procedencia, detectar_delitos, generar_sql


# Frases de ejemplo
frases = [
    "Los moros son los que más roban",
    "Los panchitos violan mujeres",
    "Los marroquis siempre están atracando",
    "Los latinos venden droga",
    "Los negros matan",
    "Los gitanos se pelean todo el día"
]

for frase in frases:
    print(f"\nFrase: {frase}")
    
    sql_por_procedencia, sql_total_general = generar_sql(frase)
    
    print("SQL por procedencia:")
    print(sql_por_procedencia)
    
    print("\nSQL total general:")
    print(sql_total_general)
