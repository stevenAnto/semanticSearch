from django.db import connection
from django.shortcuts import render
from .models import ProductoAhorro, ProductoAhorroSBS
from .serializers import EmbeddingProductoAhorroSBSSerializer, EmbeddingProductoAhorroSerializer
from sentence_transformers import SentenceTransformer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
from scipy.spatial.distance import cosine




model = SentenceTransformer('all-MiniLM-L6-v2')

class ProductoAhorroViewSet(ModelViewSet):
    queryset = ProductoAhorro.objects.all()
    serializer_class = EmbeddingProductoAhorroSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        total = queryset.count()
        return Response({
            'count': total,
            'results': serializer.data
        })

    def perform_create(self, serializer):
        data = serializer.validated_data

        texto_embedding = f"""
            Región: {data.get('region', '')}
            Tipo de cuenta: {data.get('tipo_cuenta', '')}
            Moneda: {data.get('moneda', '')}
            Saldo promedio: {data.get('saldo_promedio', '')}
            Tipo de institución: {data.get('tipo_institucion', '')}
        """

        vector_embedding = model.encode(texto_embedding).tolist()
        serializer.save(vector_embedding=vector_embedding)

    def perform_update(self, serializer):
        data = serializer.validated_data

        texto_embedding = f"""
            Región: {data.get('region', '')}
            Tipo de cuenta: {data.get('tipo_cuenta', '')}
            Moneda: {data.get('moneda', '')}
            Saldo promedio: {data.get('saldo_promedio', '')}
            Tipo de institución: {data.get('tipo_institucion', '')}
        """

        vector_embedding = model.encode(texto_embedding).tolist()
        serializer.save(vector_embedding=vector_embedding)


class BusquedaVectorialAPIView(APIView):
    def post(self, request):
        query_text = request.data.get("query", "")
        if not query_text:
            return Response({"error": "No query provided"}, status=400)

        query_vector = model.encode(query_text).tolist()
        #query_vector_pg = str(query_vector).replace('[', '{').replace(']', '}')

        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT id, nombre_entidad_financiera, tipo_cuenta, region, saldo_promedio,tasa, moneda, vector_embedding <=>CAST(%s AS vector) AS distance
                FROM productos_productoahorro
                ORDER BY distance
                LIMIT 5;
            """, [query_vector])
            rows = cursor.fetchall()

        results = [
            {
                "id": row[0],
                "tasa": float(row[5]),
                "moneda":row[6],
                "nombre_entidad_financiera": row[1],
                "tipo_cuenta": row[2],
                "region": row[3],
                "saldo_promedio": float(row[4]),
                "distance": float(row[7])
            }
            for row in rows
        ]

        return Response({
            "count": len(results),  # Número de resultados en la respuesta
            "results": results
        })


class ProductoAhorroViewSetSBS(ModelViewSet):
    queryset = ProductoAhorroSBS.objects.all()
    serializer_class = EmbeddingProductoAhorroSBSSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        total = queryset.count()
        return Response({
            'count': total,
            'results': serializer.data
        })

    def perform_create(self, serializer):
        data = serializer.validated_data
        texto_embedding = f"""
            Ubicación: {data.get('ubicacion', '')}
            Entidad: {data.get('entidad', '')}
            Tipo de cuenta: {data.get('tipo_cuenta', '')}
            Condiciones: {data.get('condiciones', '')}
            Moneda: {data.get('moneda', '')}
            Tasa: {data.get('tasa', '')}
        """
        embedding_vector = model.encode(texto_embedding).tolist()
        serializer.save(embedding=embedding_vector)

    def perform_update(self, serializer):
        data = serializer.validated_data
        texto_embedding = f"""
            Ubicación: {data.get('ubicacion', '')}
            Entidad: {data.get('entidad', '')}
            Tipo de cuenta: {data.get('tipo_cuenta', '')}
            Condiciones: {data.get('condiciones', '')}
            Moneda: {data.get('moneda', '')}
            Tasa: {data.get('tasa', '')}
        """
        embedding_vector = model.encode(texto_embedding).tolist()
        serializer.save(embedding=embedding_vector)
    
    @action(detail=False, methods=["delete"], url_path="eliminar_todos")
    def eliminar_todos(self, request):
        total = ProductoAhorroSBS.objects.count()
        ProductoAhorroSBS.objects.all().delete()
        return Response(
            {"message": f"✅ Se eliminaron {total} productos."},
            status=status.HTTP_200_OK
        )

class BusquedaVectorialSBSAPIView(APIView):
    def post(self, request):
        query_text = request.data.get("query", "")
        if not query_text:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)
        
                # Si menciona "tasa", usamos SQL primero
        if consulta_menciona_tasa(query_text):
            print("es una consulta por tasa")
            productos = obtener_productos_filtrados_por_tasa()
            #print("prodcutos",productos)

            resultados = buscar_semanticamente(query_text, productos)

            return Response({
                "query": query_text,
                "results": resultados
            }, status=200)

        # Generar embedding para la consulta
        query_embedding = model.encode(query_text).tolist()
        print(query_embedding)

        # Buscar los más similares usando pgvector (asumiendo que el campo se llama 'embedding')
        # Esto usa la distancia coseno (o el operador <-> depende de tu configuración)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, ubicacion, entidad, tasa, tipo_cuenta, condiciones, moneda, embedding
                FROM productos_productoahorrosbs
                ORDER BY embedding <#> %s::vector
                LIMIT 10;
            """, [query_embedding])
            resultados = cursor.fetchall()

        # Mapear resultados a diccionarios
        campos = ["id", "ubicacion", "entidad", "tasa", "tipo_cuenta", "condiciones", "moneda", "embedding"]
        lista_resultados = [dict(zip(campos, fila)) for fila in resultados]

        # Serializar resultados (opcional: puedes usar el serializer si quieres)
        serializer = EmbeddingProductoAhorroSBSSerializer(lista_resultados, many=True)


        return Response({
            "count":len(resultados),
            "query": query_text,
            "results": serializer.data
        }, status=status.HTTP_200_OK)



def extraer_tasa(self, texto):
    """Extrae un número decimal (tasa) del texto si existe"""
    import re
    match = re.search(r"\b(\d+\.\d+)\b", texto)
    if match:
        return float(match.group(1))
    return None

def consulta_menciona_tasa(query_text):
    return "tasa" in query_text.lower()

def obtener_productos_filtrados_por_tasa():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, ubicacion, entidad, tasa, tipo_cuenta, condiciones, moneda
            FROM productos_productoahorrosbs
            WHERE tasa IS NOT NULL AND tasa > 0
            ORDER BY tasa DESC
            LIMIT 100;
        """)
        filas = cursor.fetchall()

    campos = ["id", "ubicacion", "entidad", "tasa", "tipo_cuenta", "condiciones", "moneda"]
    return [dict(zip(campos, fila)) for fila in filas]

def construir_texto(producto):
    return f"Cuenta en {producto['moneda']} con tasa de {producto['tasa']}%. Condiciones: {producto['condiciones']}."   

def buscar_semanticamente(query_text, productos, top_k=10):
    query_embedding = model.encode(query_text)
    resultados = []

    for p in productos:
        texto = construir_texto(p)
        emb = model.encode(texto)
        sim = 1 - cosine(query_embedding, emb)
        p["score"] = round(sim, 4)
        resultados.append(p)

    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados[:top_k]