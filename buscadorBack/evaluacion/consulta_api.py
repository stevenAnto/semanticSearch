
import json
import requests

API_URL = "http://127.0.0.1:8000/busquedaVectorialSBS/"  # Ajusta al URL de tu API

# Cargar las queries desde el JSON
with open("./evaluacion.json", "r") as f:
    queries = json.load(f)

resultados = []

for item in queries:
    query_text = item["query"]
    payload = {"query": query_text}
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            resultados.append({
                "query": query_text,
                "results": data.get("results", [])
            })
            print(f"✅ Query '{query_text}' procesada.")
        else:
            print(f"❌ Error {response.status_code} en query '{query_text}': {response.text}")
    except Exception as e:
        print(f"❌ Excepción en query '{query_text}': {e}")

# Guardar resultados en JSON
with open("resultados.json", "w") as f:
    json.dump(resultados, f, indent=2)

print("✅ Resultados guardados en resultados.json")
