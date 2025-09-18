from django.db import models

# Create your models here.

class AcuerdoDetalle(models.Model): #la parte operativa
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

    def __str__(self):
        return f"{self.numerador} - {self.descripcion[:20]}"

class AcuerdoDirectivo(models.Model):  # la parte directiva
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

    def __str__(self):
        return f"{self.numerador} - {self.descripcion[:20]}"
    
class Integrante(models.Model):
    rol = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.rol
