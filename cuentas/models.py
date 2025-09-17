from django.db import models

# Create your models here.

class AcuerdoDetalle(models.Model):
    numerador = models.IntegerField()
    tipo_unidad = models.CharField(max_length=100)  # luego podrás usar choices si quieres
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
