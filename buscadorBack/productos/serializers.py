from rest_framework import serializers
from .models import ProductoAhorro, ProductoAhorroSBS


class EmbeddingProductoAhorroSerializer(serializers.ModelSerializer):
    vector_embedding = serializers.ListField(
        child=serializers.FloatField(),
        required=False,
        write_only = True
    )

    class Meta:
        model = ProductoAhorro
        fields = '__all__'  # Incluy

class EmbeddingProductoAhorroSBSSerializer(serializers.ModelSerializer):
    embedding = serializers.ListField(
        child=serializers.FloatField(),
        required=False,
        write_only = True
    )

    class Meta:
        model = ProductoAhorroSBS
        fields = '__all__'  