import json


def extraer_valores_resultado(criterio, resultados, relevantes):
    valores = []

    for item in resultados:
        if criterio == "tasa_minima":
            try:
                tasa = float(item.get("tasa", 0))
                if tasa >= relevantes[0]:  # solo un valor numérico
                    valores.append(tasa)
            except:
                continue

        elif criterio == "ubicacion_condiciones":
            esperado = relevantes
            if (item.get("ubicacion", "").lower() == esperado["ubicacion"].lower() and
                "sin mantenimiento" in item.get("condiciones", "").lower()):
                valores.append(item["id"])  # usamos el ID como marcador válido

        elif criterio == "ubicacion_tasa":
            esperado = relevantes
            try:
                tasa = float(item.get("tasa", 0))
                if (item.get("ubicacion", "").lower() == esperado["ubicacion"].lower() and
                    tasa >= esperado["tasa_minima"]):
                    valores.append(item["id"])
            except:
                continue

        else:  # Criterios simples
            valor = item.get(criterio)
            if valor in relevantes:
                valores.append(valor)

    return valores

def precision_at_k(resultados, relevantes, k=None):
    """
    Calcula la precision@k.

    Parámetros:
    - resultados: lista con los elementos obtenidos en el ranking (pueden estar repetidos).
    - relevantes: conjunto o lista con los elementos relevantes correctos.
    - k: cantidad de primeros resultados a evaluar. Si es None, se evalúan todos los resultados.

    Retorna:
    - precision: número entre 0 y 1 con la precisión calculada.
    """
    if k is not None:
        resultados = resultados[:k]
    
    relevantes_set = set(relevantes)
    resultados_relevantes = [r for r in resultados if r in relevantes_set]
    
    if len(resultados) == 0:
        return 0.0
    
    precision = len(resultados_relevantes) / len(resultados)
    return precision

def recall_at_k(relevantes, resultados, k):
    """
    Calcula Recall@k: proporción de elementos relevantes que aparecen en el top-k de resultados.

    Args:
        relevantes (list): Lista de valores relevantes (e.g., ['AYACUCHO'])
        resultados (list): Lista de resultados devueltos (e.g., ['AYACUCHO', 'LIMA', ...])
        k (int): Número de resultados a considerar

    Returns:
        float: Valor de Recall@k entre 0 y 1
    """
    relevantes = set(r.upper() for r in relevantes)
    resultados_topk = set(r.upper() for r in resultados[:k])
    
    if not relevantes:
        return 0.0

    return len(relevantes & resultados_topk) / len(relevantes)

def average_precision(relevantes, resultados):
    relevantes = set(relevantes)
    score = 0.0
    num_hits = 0
    hits = set()  # para contar hits únicos

    for i, r in enumerate(resultados, start=1):
        if r in relevantes and r not in hits:
            num_hits += 1
            score += num_hits / i
            hits.add(r)

    if num_hits == 0:
        return 0.0
    return score / len(relevantes)

def normalize_text(text):
    return text.strip().upper() if isinstance(text, str) else text  


def recall_at_k_counting(relevantes, resultados, k):
    """
    Calcula Recall@k contando todas las apariciones repetidas de elementos relevantes en los resultados.

    Args:
        relevantes (list): Lista de valores relevantes (puede tener un solo elemento).
        resultados (list): Lista de resultados devueltos.
        k (int): Número de resultados a considerar.

    Returns:
        float: Valor de recall contando repeticiones, entre 0 y 1.
    """
    print("resultados",resultados)
    relevantes = [r.upper() for r in relevantes]
    resultados_topk = [r.upper() for r in resultados[:k]]
    #print("relevantes",relevantes)
    #print("resultados_topk",relevantes)

    # Contar cuántas veces aparecen relevantes en resultados (con repeticiones)
    count_relevantes_en_resultados = sum(1 for r in resultados_topk if r in relevantes)
    #print("count_relevantes",count_relevantes_en_resultados)

    # Normalizar por k o por total relevantes (depende)
    # Aquí normalizamos por k, que es total resultados evaluados
    return count_relevantes_en_resultados / k

def porcentaje_superan_minimo(valores, minimo=4):
    total = len(valores)
    if total == 0:
        return 0.0
    count = sum(1 for v in valores if v >= minimo)
    return (count / total) * 100

def cumple_criterios(item, criterios):
    for campo, valor in criterios.items():
        if campo not in item:
            return False

        item_val = str(item[campo]).lower()
        criterio_val = str(valor).lower()

        # Heurística especial para condiciones como "sin mantenimiento"
        if campo == "condiciones" and "sin mantenimiento" in criterio_val:
            if "sin cobro" in item_val and "mantenimiento" in item_val:
                continue
            else:
                return False
        else:
            if criterio_val not in item_val:
                return False

    return True
def porcentaje_cumplen_criterios(resultados_raw, criterios_relevantes):
    if not resultados_raw:
        return 0.0

    count = sum(1 for item in resultados_raw if cumple_criterios(item, criterios_relevantes))
    return (count / len(resultados_raw)) * 100

def evaluar(evaluacion_path, resultados_path, k=10):
    with open(evaluacion_path, "r") as f:
        consultas = json.load(f)

    with open(resultados_path, "r") as f:
        resultados = json.load(f)

    aps, pks, rks = [], [], []

    for consulta in consultas:
        query = consulta["query"]
        criterio = consulta["criterio"]
        relevantes = consulta["relevantes"]
        print("creterios",criterio)

        res_consulta = next((r for r in resultados if r["query"] == query), None)
        if res_consulta is None:
            print(f"❌ No hay resultados para: {query}")
            continue

        resultados_raw = res_consulta["results"]
        if criterio == "tasa_minima":
            print("entro a tasa minimo")

            # Extraer tasas relevantes (por ejemplo, las mínimas aceptables)
            ids_relevantes = extraer_valores_resultado(criterio, resultados_raw, relevantes)

            # Extraer las tasas desde los resultados
            resultados_valores = [item["tasa"] for item in resultados_raw]

            # Usamos la primera tasa de referencia (puedes adaptarlo si hay más)
            umbral_minimo = ids_relevantes[0]
            #print("resultados valor",resultados_valores)

            # Llamamos a la función con las tasas y el umbral
            porcentaje = porcentaje_superan_minimo(resultados_valores, umbral_minimo)

            print(f"Porcentaje que supera {umbral_minimo}: {porcentaje:.2f}%")

        elif criterio == "ubicacion_condiciones":
            print("entro a ubicacion_condiciones")

            criterios_relevantes = relevantes  # ya viene como dict: {"ubicacion": ..., "condiciones": ...}
           #print("resultados_war",resultados_raw)
            #print("crieteios",criterios_relevantes)
            porcentaje = porcentaje_cumplen_criterios(resultados_raw, criterios_relevantes)

            print(f"Porcentaje que cumple criterios {criterios_relevantes}: {porcentaje:.2f}%")        
        else:
            # Criterios simples: extraer y normalizar valores del campo específico
            resultados_valores = [
                normalize_text(item.get(criterio)) for item in resultados_raw 
                if criterio in item and item.get(criterio) is not None
            ]
            # Normalizar valores relevantes
            relevantes_valores = [normalize_text(r) for r in relevantes]
        
            # Debug: imprimir listas
            print(f"\nQuery: {query}")
            print(f"Criterio: {criterio}")
            #print(f"Relevantes originales: {relevantes}")
            #print(f"IDs/valores relevantes: {relevantes_valores}")
            #print(f"IDs/valores resultados (top {k}): {resultados_valores[:k]}")
            
            # Calcular métricas
            rck =recall_at_k_counting(relevantes_valores,resultados_valores,k)


            print(f" rck : {rck:.3f} ")
            print("-" * 50)


evaluar("evaluacion.json", "resultados.json", k=10)
