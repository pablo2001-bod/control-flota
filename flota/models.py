import os
from django.db import models
from django.db.models.signals import post_delete  
from django.dispatch import receiver              

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


@receiver(post_delete, sender=Vehiculo)
def eliminar_foto_vehiculo_al_borrar(sender, instance, **kwargs):
    if instance.foto and os.path.isfile(instance.foto.path):
        os.remove(instance.foto.path)

@receiver(post_delete, sender=Mantenimiento)
def eliminar_pdf_mantenimiento_al_borrar(sender, instance, **kwargs):
    if instance.pdf_diagnostico and os.path.isfile(instance.pdf_diagnostico.path):
        os.remove(instance.pdf_diagnostico.path)