from django.db import models

class Vehiculo(models.Model):
    placa = models.CharField(max_length=20, unique=True)
    tipo_vehiculo = models.CharField(max_length=30)  # Sedán, Camioneta, Camión
    tipo_combustible = models.CharField(max_length=20)  # Gasolina, Diésel, Eléctrico
    seguro_vigente = models.BooleanField(default=False)  # Checkbox
    anio_modelo = models.IntegerField()
    foto = models.ImageField(upload_to='vehiculos/', null=True, blank=True)

    def __str__(self):
        return self.placa

class Mantenimiento(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='mantenimientos')
    fecha_servicio = models.DateField()
    costo_taller = models.FloatField()
    tipo_mantenimiento = models.CharField(max_length=20)  # Preventivo, Correctivo
    repuestos_cambiados = models.TextField()
    pdf_diagnostico = models.FileField(upload_to='mantenimientos/', null=True, blank=True)

    def __str__(self):
        return f"Mantenimiento #{self.id} - {self.vehiculo.placa}"