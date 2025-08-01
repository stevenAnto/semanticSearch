import pandas as pd
import requests

# Cargar archivo
df = pd.read_csv("./data/productos_ahorro_sbs.csv")  # ajusta esto
#df = df.head(5)

# URL de tu API Django (ajusta si usas localhost, ngrok, etc.)
API_URL = "http://127.0.0.1:8000/buscadoSBS/"  # o como esté configurado

# Iterar y enviar productos uno por uno
for i, row in df.iterrows():
    data = {
        "ubicacion": row["ubicacion"],
        "entidad": row["entidad"],
        "tasa": float(row["tasa"]),
        "tipo_cuenta": row["tipo_cuenta"],
        "condiciones": row["condiciones"],
        "moneda": row["moneda"]
    }

    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            print(f"✅ {i + 1}: {row['entidad']} registrado.")
        else:
            print(f"❌ {i + 1}: Error ({response.status_code}) - {response.text}")
    except Exception as e:
        print(f"❌ {i + 1}: Fallo de red - {e}")
