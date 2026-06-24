from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=20, unique=True)
    tipo_vehiculo = models.CharField(max_length=50)  # Sedán/Camioneta/Camión
    tipo_combustible = models.CharField(max_length=30)  # Gasolina/Diésel/Eléctrico
    seguro_vigente = models.BooleanField(default=False)
    anio_modelo = models.IntegerField()
    foto = models.ImageField(upload_to='vehiculos/', null=True, blank=True)

    def __str__(self):
        return self.placa

class Mantenimiento(models.Model):
    fecha_servicio = models.DateField()
    costo_taller = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_mantenimiento = models.CharField(max_length=30)  # Preventivo/Correctivo
    repuestos_cambiados = models.TextField()
    pdf_diagnostico = models.FileField(upload_to='mantenimientos/', null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_mantenimiento} - {self.fecha_servicio}"