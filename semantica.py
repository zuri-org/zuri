import re
import unicodedata

# Patrones de procedencia (incluye términos peyorativos y generales)
patrones_procedencia = [
    # África / Magreb
    (r"\b(moro|moros|marroqui|marroquies|marroquíes|marroquí|moromierda|magreb[ií]([ae]s)?|marroqu[ií]([ae]s)?|terroristas|musulmán|musulman|mohamed|mohameds|segarro|amego|patera|pateras|paterista|mena|menas|sin papeles|inmigrante ilegal|mantero|manteros|subsahariano|subsaharianos|clandestino|clandestinos|africano|africanos|guineano|guineanos|negro|negros|negrata|negratas|esclavo|esclavos|tribal|tribales|de la tribu|de la selva|parásito|parásitos|mantenido|mantenidos|pobre|pobres|analfabeto|analfabetos|incivilizado|incivilizados|salvaje|salvajes|bárbaro|bárbaros|cachorro|cachorros|exótico|exóticos)\b", 
     "África"),

    # América Latina
    (r"\b(sudaca|sudacas|latino|latinos|latina|latinas|latinoamericano|latinoamericanos|panchito|panchitos|machupichu|machupichus|hispano|hispanos|peruano|peruanos|colombiano|colombianos|venezolano|venezolanos|boliviano|bolivianos)\b", 
     "América"),

    # Europa (prejuicio étnico: gitanos)
    (r"\b(blancos pobres|basura blanca|chabolistas)\b", 
     "Europa"),

    # Asia / Medio Oriente
    (r"\b(chinos|chino|amarillo|oriental|orientales|asiatico|oriental)\b",
     "Asia"),

    # ESPAÑOLA
    (r"\b(español[ae]s?)\b", "Española"),

    # AFRICA
    (r"\b(argelinos?|argelia)\b", "África"),
    (r"\b(angoleños?|angola)\b", "África"),
    (r"\b(benineses?|benín)\b", "África"),
    (r"\b(botsuano?|botsuana)\b", "África"),
    (r"\b(burkineses?|burkina\s+faso)\b", "África"),
    (r"\b(burundeses?|burundi)\b", "África"),
    (r"\b(cabo\s+verdianos?|cabo\s+verde)\b", "África"),
    (r"\b(cameruneses?|camerún)\b", "África"),
    (r"\b(centroafricanos?|república\s+centroafricana)\b", "África"),
    (r"\b(comorenses?|comoras)\b", "África"),
    (r"\b(congoleños?|congo)\b", "África"),
    (r"\b(marfileños?|costa\s+de\s+marfil)\b", "África"),
    (r"\b(egipcios?|egipto)\b", "África"),
    (r"\b(eritreos?|eritrea)\b", "África"),
    (r"\b(etíopes?|etiopía)\b", "África"),
    (r"\b(gaboneses?|gabón)\b", "África"),
    (r"\b(gambianos?|gambia)\b", "África"),
    (r"\b(ghaneses?|ghana)\b", "África"),
    (r"\b(guineanos?|guinea)\b", "África"),
    (r"\b(ecuatoguineanos?|guinea\s+ecuatorial)\b", "África"),
    (r"\b(guineanos\s+bissaus?|guinea-bisáu)\b", "África"),
    (r"\b(kenianos?|kenia)\b", "África"),
    (r"\b(lesotenses?|lesoto)\b", "África"),
    (r"\b(liberianos?|liberia)\b", "África"),
    (r"\b(libios?|libia)\b", "África"),
    (r"\b(malauíes?|malaui)\b", "África"),
    (r"\b(malienses?|malí)\b", "África"),
    (r"\b(marroquíes?|marruecos)\b", "África"),
    (r"\b(mauritanos?|mauritania)\b", "África"),
    (r"\b(mauricianos?|mauricio)\b", "África"),
    (r"\b(mozambiqueños?|mozambique)\b", "África"),
    (r"\b(namibios?|namibia)\b", "África"),
    (r"\b(nigerinos?|níger)\b", "África"),
    (r"\b(nigerianos?|nigeria)\b", "África"),
    (r"\b(ruandeses?|ruanda)\b", "África"),
    (r"\b(santotomenses?|santo\s+tomé\s+y\s+príncipe)\b", "África"),
    (r"\b(senegaleses?|senegal)\b", "África"),
    (r"\b(seychellenses?|seychelles)\b", "África"),
    (r"\b(sierraleoneses?|sierra\s+leona)\b", "África"),
    (r"\b(somalienses?|somalia)\b", "África"),
    (r"\b(suazilandeses?|suazilandia)\b", "África"),
    (r"\b(sudafricanos?|sudáfrica)\b", "África"),
    (r"\b(sudaneses?|sudán)\b", "África"),
    (r"\b(sudaneses\s+del\s+sur?|sudán\s+del\s+sur)\b", "África"),
    (r"\b(tanzanos?|tanzania)\b", "África"),
    (r"\b(togoleses?|togo)\b", "África"),
    (r"\b(tunecinos?|túnez)\b", "África"),
    (r"\b(ugandeses?|uganda)\b", "África"),
    (r"\b(yibutienses?|yibuti)\b", "África"),
    (r"\b(zambianos?|zambia)\b", "África"),
    (r"\b(zimbabuenses?|zimbabue)\b", "África"),  

    # AMERICA (norte, centro, sur)
    (r"\b(estadounidenses?|estados\s+unidos)\b", "América"),
    (r"\b(canadienses?|canadá)\b", "América"),
    (r"\b(mexicanos?|méxico)\b", "América"),
    (r"\b(beliceños?|belice)\b", "América"),
    (r"\b(costarricenses?|costa\s+rica)\b", "América"),
    (r"\b(salvadoreños?|el\s+salvador)\b", "América"),
    (r"\b(guatemaltecos?|guatemala)\b", "América"),
    (r"\b(hondureños?|honduras)\b", "América"),
    (r"\b(nicaragüenses?|nicaragua)\b", "América"),
    (r"\b(panameños?|panamá)\b", "América"),
    (r"\b(antiguos?|antigua\s+y\s+barbuda)\b", "América"),
    (r"\b(bahameños?|bahamas)\b", "América"),
    (r"\b(barbadenses?|barbados)\b", "América"),
    (r"\b(cubanos?|cuba)\b", "América"),
    (r"\b(dominiqueses?|dominica)\b", "América"),
    (r"\b(dominicanos?|rep[.á\s]*dominicana)\b", "América"),
    (r"\b(granadinos?|granada)\b", "América"),
    (r"\b(haitianos?|haití)\b", "América"),
    (r"\b(jamaicanos?|jamaica)\b", "América"),
    (r"\b(san\s+cristobaleños?|san\s+cristóbal\s+y\s+nieves)\b", "América"),
    (r"\b(san\s+vicentinos?|san\s+vicente\s+y\s+las\s+granadinas)\b", "América"),
    (r"\b(santalucenses?|santa\s+lucía)\b", "América"),
    (r"\b(trinitenses?|trinidad\s+y\s+tobago)\b", "América"),
    (r"\b(argentinos?|argentina)\b", "América"),
    (r"\b(bolivianos?|bolivia)\b", "América"),
    (r"\b(brasileños?|brasil)\b", "América"),
    (r"\b(chilenos?|chile)\b", "América"),
    (r"\b(colombianos?|colombia)\b", "América"),
    (r"\b(ecuatorianos?|ecuador)\b", "América"),
    (r"\b(guyaneses?|guyana)\b", "América"),
    (r"\b(paraguayos?|paraguay)\b", "América"),
    (r"\b(peruanos?|perú)\b", "América"),
    (r"\b(surinameses?|surinam)\b", "América"),
    (r"\b(uruguayos?|uruguay)\b", "América"),
    (r"\b(venezolanos?|venezuela)\b", "América"),

    # EUROPA (excluyendo España)
    (r"\b(albaneses?|albania)\b", "Europa"),
    (r"\b(alemanes?|alemania)\b", "Europa"),
    (r"\b(andorranos?|andorra)\b", "Europa"),
    (r"\b(austriacos?|austria)\b", "Europa"),
    (r"\b(bielorrusos?|bielorrusia)\b", "Europa"),
    (r"\b(bélgicos?|bélgica)\b", "Europa"),
    (r"\b(bosnios?|bosnia\s+y\s+herzegovina)\b", "Europa"),
    (r"\b(búlgaros?|bulgaria)\b", "Europa"),
    (r"\b(croatas?|croacia)\b", "Europa"),
    (r"\b(chipriotas?|chipre)\b", "Europa"),
    (r"\b(checos?|república\s+checa)\b", "Europa"),
    (r"\b(daneses?|dinamarca)\b", "Europa"),
    (r"\b(eslovacos?|eslovaquia)\b", "Europa"),
    (r"\b(eslovenos?|eslovenia)\b", "Europa"),
    (r"\b(estonios?|estonia)\b", "Europa"),
    (r"\b(finlandeses?|finlandia)\b", "Europa"),
    (r"\b(franceses?|francia)\b", "Europa"),
    (r"\b(griegos?|grecia)\b", "Europa"),
    (r"\b(húngaros?|hungría)\b", "Europa"),
    (r"\b(irlandeses?|irlanda)\b", "Europa"),
    (r"\b(islandeses?|islandia)\b", "Europa"),
    (r"\b(italianos?|italia)\b", "Europa"),
    (r"\b(letones?|letonia)\b", "Europa"),
    (r"\b(liechtensteinianos?|liechtenstein)\b", "Europa"),
    (r"\b(lituanos?|lituania)\b", "Europa"),
    (r"\b(luxemburgueses?|luxemburgo)\b", "Europa"),
    (r"\b(macedonios?|macedonia\s+del\s+norte)\b", "Europa"),
    (r"\b(malteses?|malta)\b", "Europa"),
    (r"\b(moldavos?|moldavia)\b", "Europa"),
    (r"\b(monegascos?|mónaco)\b", "Europa"),
    (r"\b(montenegrinos?|montenegro)\b", "Europa"),
    (r"\b(noruegos?|noruega)\b", "Europa"),
    (r"\b(holandeses?|países\s+bajos)\b", "Europa"),
    (r"\b(polacos?|polonia)\b", "Europa"),
    (r"\b(portugueses?|portugal)\b", "Europa"),
    (r"\b(ingleses?|británicos?|reino\s+unido)\b", "Europa"),
    (r"\b(rumanos?|rumanía)\b", "Europa"),
    (r"\b(rusos?|rusia)\b", "Europa"),
    (r"\b(sanmarinenses?|san\s+marino)\b", "Europa"),
    (r"\b(serbios?|serbia)\b", "Europa"),
    (r"\b(suecos?|suecia)\b", "Europa"),
    (r"\b(suizos?|suiza)\b", "Europa"),
    (r"\b(ucranianos?|ucrania)\b", "Europa"),
    (r"\b(vaticanos?|ciudad\s+del\s+vaticano)\b", "Europa"),

    # ASIA
    (r"\b(chinos?|china)\b", "Asia"),
    (r"\b(indios?|india)\b", "Asia"),
    (r"\b(paquistan[ií]es?|pakistán)\b", "Asia"),
    (r"\b(banglades[ií]es?|bangladesh)\b", "Asia"),
    (r"\b(filipinos?|filipinas)\b", "Asia"),

    # OCEANÍA
    (r"\b(australianos?|australia)\b", "Oceanía"),
    (r"\b(neozelandeses?|nueva\s+zelanda)\b", "Oceanía"),

    # APÁTRIDAS Y OTROS
    (r"\b(apátridas?|sin\s+nacionalidad)\b", "Apátridas"),
    (r"\b(extranjeros?|extranjera|extranjero)\b", "Extranjera"),
]


# Patrones de delitos con sinónimos y expresiones coloquiales
patrones_delitos = [
    # Homicidio y derivados
    (r"\b(matar|matan|mató|asesinar|asesinan|asesinó|liquidar|liquidan|ejecutar|ejecutaron|cargarse|homicidio|homicidios|asesinato|asesinatos)\b",
     ["Homicidio", "Asesinato", "Homicidio por imprudencia", "Inducción al suicidio"]),

    # Lesiones / peleas
    (r"\b(pelear|pelea|pelean|se pelean|hostias|paliza|palizas|guantazo|guantazos|tortazo|tortazos|curtir el lomo|dejar KO|golpear|altercados en la vida publica|golpean|golpes|agredir|agresión|violentos|agreden)\b",
     ["Lesiones"]),

    # Contra la libertad
    (r"\b(secuestrar|secuestran|retención|retener|coaccionar|coaccionan|chantajear|chantajean|amenazar|amenazan|meter miedo|intimidar)\b",
     ["Amenazas", "Coacciones y detenciones ilegales"]),

    # Torturas e integridad moral
    (r"\b(maltratar|maltratan|meter miedo|meten miedo|tortura psicologica|humillar|humillan|vejar|vejan|abusar|abusan|torturar|torturan|ensañarse|cruel|trato degradante|trato inhumano)\b",
     ["Trato degradante y violencia", "Tortura"]),

    # Contra la libertad e indemnidad sexuales
    (r"\b(violar|violan|violó|violación|abusar sexualmente|abuso sexual|maltratan|maltrato|meten mano|abusos sexuales|agredir sexualmente|agresión sexual|manosear|manosean|tocamientos|toquetear)\b",
     ["Contra la libertad e indemnidad sexuales"]),

    # Contra el patrimonio 1 (robos, hurtos, etc.)
    (r"\b(robar|roban|robó|robo|robos|cometen robos|asalto|asaltos|vivir de lo ajeno|roban|ladrones|ladrón|hurtar|crimenes violentos|hurto|hurta|asaltar|asaltan|atracar|atracan|atracando|atraco|allanamiento|choricean|hurtan)\b",
     ["Hurtos", "Robos", "Robo con violencia", "Robo con fuerza", "Robo y hurto de uso de vehículo"]),
    
    # Contra el patrimonio 2 (usurpación, blanqueo de capitales, etc.)
    (r"\b(estafar|estafando|estafa|timar|timo|blanquear|receptar|apropiar|apropian|estafan|estafas|receptan|defraudan|usurpan|ocupación|opcupaciones|usuarpacion|blanquean|lavan dinero)\b",
     ["Usurpación", "Defraudaciones", "Estafas", "Apropiación indebida", "Daños", "Receptación y blanqueo de capitales"]),

    # Contra la seguridad colectiva (droga, tráfico, etc.)
    (r"\b(droga|traficar con drogas|tráfico de drogas|trapichear|trapicheo|trafican|venden droga|fumarse un porro|colocarse|camello)\b",
     ["Contra la salud pública", "Contra la seguridad vial"]),

    # Contra la autoridad u orden público
    (r"\b(altercado|bronca|desorden|liarla|liarla parda|reventar|disturbios|desobedecer|resistirse|resisten|manifestarse violentamente|enfrentarse a la policía)\b",
     ["Atentados contra la autoridad y de la resistencia y desobediencia", "Atentados contra la autoridad", "Resistencia y desobediencia"]),

    # Contra la seguridad vial
    (r"\b(conducir borracho|conducen borrachos|conducen drogados|conducen mal|alcoholizado|drogado|sin carnet|hacer trompos|accidente de tráfico|coche a toda velocidad|conducción temeraria)\b",
     ["Contra la seguridad vial"]),

    # Falsedades
    (r"\b(falsificar|papeles falsos|dni falso|documento falso|engañar con documentación)\b",
     ["Falsedades documentales", "Fasificación documentos públicos", "Falsificación de certificados"]),

    # Corrupción o delitos de administración
    (r"\b(corrupto|corrupción|soborno|cohecho|prevaricar|enchufe político|no auxilian|auxilio|no colaborar|no colaboran|chanchullo)\b",
     ["Desobediencia y denegación auxilio", "Otros delitos contra la Administración Pública"]),

    # Contra la Administración de Justicia
    (r"\b(denunciar en falso|mienten a la autoridad|acusación falsa|simular delito|denuncia falsa| denuncias falsas|mentir en denuncia|quebrantamiento de condena)\b",
     ["Acusación y denuncia falsas y simulación de delitos", "Acusación y denuncias falsas", "Simulación del delito", "Quebrantamiento de condena", "Otros delitos contra la Administración de Justicia"]),

     # Contra las relaciones familiares
    (r"\b(relacion familiar|relaciones familiares|malas relaciones familiares|abandonan|hijo|hija|hijos|hijas|abandonar|abandona|negligencia parental)\b",
     ["Abandono de familia", "Contra los derechos y deberes familiares", "Quebrantamiento de los deberes de custodia"]),

     # Otros genéricos
    (r"\b(delito|delincuente|delincuencia|crimen|criminal|delincuentes)\b",
     ["Resto de delitos"])
]

# Normalizar texto

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    return texto



def detectar_procedencia(frase):
    frase = normalizar_texto(frase)
    procedencias_detectadas = set()
    for patron, procedencia in patrones_procedencia:
        if re.search(patron, frase):
            procedencias_detectadas.add(procedencia)
    if procedencias_detectadas:
        procedencias_detectadas.add("Española")

    return list(procedencias_detectadas)


def detectar_delitos(frase):
    frase = normalizar_texto(frase)
    delitos_detectados = set()
    for patron, delitos in patrones_delitos:
        if re.search(patron, frase):
            delitos_detectados.update(delitos)
    return list(delitos_detectados)


def generar_sql(frase):
    delitos = detectar_delitos(frase)
    procedencias_detectadas = detectar_procedencia(frase)

    if procedencias_detectadas == ["Española"]:
        procedencias_detectadas = [] 

    
    if not delitos:
        return "-- NO_DETECTADO", "-- NO_DETECTADO"

    delitos = sorted(delitos)
    # Caso 1: Hay delito pero no procedencias
    if not procedencias_detectadas:
        sql_por_procedencia = (
            "SELECT Procedencia, TipoDelito, Valor AS Total\n"
            "FROM delitos\n"
            f"WHERE TipoDelito IN ({', '.join(repr(d) for d in delitos)})\n"
            "ORDER BY Total DESC;"
        )

    else:
        # Caso 2: Hay delito y procedencias — agregar Española y Total si no están
        procedencias = set(procedencias_detectadas)
        procedencias.update(["Española", "Total"])
        procedencias = sorted(procedencias)

        sql_por_procedencia = (
            "SELECT Procedencia, TipoDelito, Valor AS Total\n"
            "FROM delitos\n"
            f"WHERE TipoDelito IN ({', '.join(repr(d) for d in delitos)})\n"
            f"AND Procedencia IN ({', '.join(repr(p) for p in procedencias)})\n"
            "ORDER BY Total DESC;"
        )


    # Consulta del total general del delito (sin procedencias)
    sql_total_general = (
        "SELECT TipoDelito, Valor AS Total\n"
        "FROM delitos\n"
        f"WHERE TipoDelito IN ({', '.join(repr(d) for d in delitos)})\n"
        "AND Procedencia = 'Total'\n"
        "ORDER BY Total DESC;"
    )

    return sql_por_procedencia, sql_total_general
