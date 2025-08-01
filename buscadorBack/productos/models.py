from django.db import models
from pgvector.django import VectorField

from django.db import models
from pgvector.django import VectorField

class ProductoAhorro(models.Model):
    TASA_MAX_DIGITS = 5
    TASA_DECIMAL_PLACES = 2

    # Campos con opciones limitadas (choices)
    REGIONES = [
        ('amazonas', 'Amazonas'),
        ('ancash', 'Ancash'),
        ('apurimas', 'Apurímac'),
        ('arequipa', 'Arequipa'),
        ('ayacucho', 'Ayacucho'),
        ('cajamarca', 'Cajamarca'),
        ('cusco', 'Cusco'),
        ('huancavelica', 'Huancavelica'),
        ('huanuco', 'Huánuco'),
        ('ica', 'Ica'),
        ('junin', 'Junín'),
        ('la libertad', 'La Libertad'),
        ('lima', 'Lima'),
        ('loreto', 'Loreto'),
        ('madre de dios', 'Madre de Dios'),
        ('moquegua', 'Moquegua'),
        ('pasco', 'Pasco'),
        ('piura', 'Piura'),
        ('puno', 'Puno'),
        ('san martin', 'San Martín'),
        ('tacna', 'Tacna'),
        ('tumbes', 'Tumbes'),
        ('ucayali', 'Ucayali'),
        ('lima provincia', 'Lima Provincia'),  # Nota: Lima aparece dos veces, cambia si quieres
    ]

    TIPO_CUENTA_CHOICES = [
        ('CTS', 'CTS'),
        ('sueldo', 'Sueldo'),
        ('ahorro', 'Ahorro'),
    ]

    MONEDA_CHOICES = [
        ('soles', 'Soles'),
        ('dolares', 'Dólares'),
    ]

    TIPO_INSTITUCION_CHOICES = [
        ('banco', 'Banco'),
        ('caja', 'Caja'),
        ('financiera', 'Financiera'),
    ]

    tasa = models.DecimalField(
        max_digits=TASA_MAX_DIGITS, decimal_places=TASA_DECIMAL_PLACES,
        null=True, blank=True,
        help_text="Tasa en porcentaje, ejemplo 3.50"
    )
    nombre_entidad_financiera = models.CharField(max_length=255)

    ##Para embbeding
    region = models.CharField(max_length=20, choices=REGIONES, default='lima')
    moneda = models.CharField(max_length=10, choices=MONEDA_CHOICES, default='soles')
    tipo_cuenta = models.CharField(max_length=10, choices=TIPO_CUENTA_CHOICES, default='ahorro')
    tipo_institucion = models.CharField(max_length=15, choices=TIPO_INSTITUCION_CHOICES, default='banco')
    saldo_promedio = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)



    vector_embedding = VectorField(dimensions=384, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_entidad_financiera} - {self.tipo_cuenta} - {self.region}"

class ProductoAhorroSBS(models.Model):
    ubicacion = models.CharField(max_length=100)
    entidad = models.CharField(max_length=200)
    tasa = models.DecimalField(max_digits=5, decimal_places=3)
    tipo_cuenta = models.CharField(max_length=100)
    condiciones = models.CharField(max_length=200)
    moneda = models.CharField(max_length=100)

    # Campo vectorial para almacenar embedding, dimensión depende del modelo que uses (ejemplo 384)
    embedding = VectorField(dimensions=384)

    def __str__(self):
        return f"{self.entidad} - {self.ubicacion}"
