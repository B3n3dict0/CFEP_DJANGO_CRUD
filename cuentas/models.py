from django.db import models

# -----------------------
# MODELO OPERATIVA
# -----------------------
class AcuerdoOperativa(models.Model):
    numerador = models.IntegerField()
    tipo_unidad = models.CharField(max_length=100)  
    descripcion = models.TextField()
    unidad_parada = models.BooleanField(default=False)
    fecha_limite = models.DateField()
    pendiente = models.BooleanField(default=True)
    responsable = models.CharField(max_length=100)
    porcentaje_avance = models.PositiveIntegerField()  # solo números positivos

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acuerdos_operativa'  # asegura que sea una tabla separada
        ordering = ['numerador']

    def __str__(self):
        return f"{self.numerador} - {self.descripcion[:20]}"

# -----------------------
# MODELO DIRECTIVA
# -----------------------
class AcuerdoDirectiva(models.Model):
    numerador = models.IntegerField()
    tipo_unidad = models.CharField(max_length=100)  # texto del área
    descripcion = models.TextField()  # acuerdo escrito
    unidad_parada = models.BooleanField(default=False)
    fecha_limite = models.DateField()
    pendiente = models.BooleanField(default=True)
    responsable = models.CharField(max_length=100)
    responsable_manual = models.CharField(max_length=100, blank=True, null=True)  # para "Otro..."
    porcentaje_avance = models.PositiveIntegerField()  # solo números positivos

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'acuerdos_directiva'  # asegura que sea una tabla separada
        ordering = ['numerador']

    def __str__(self):
        return f"{self.numerador} - {self.descripcion[:20]}"

# -----------------------
# MODELO INTEGRANTES
# -----------------------
class Integrante(models.Model):
    rol = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'integrantes'

    def __str__(self):
        return self.rol
