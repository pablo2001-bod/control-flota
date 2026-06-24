import os
from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import Vehiculo, Mantenimiento

def inicio(request):
    return render(request, 'index.html')

def NuevoVehiculo(request):
    return render(request, 'NuevoVehiculo.html')

def guardarVehiculo(request):
    if request.method == "POST":
        placa_val = request.POST["placa"]
        tipo_vehiculo_val = request.POST["tipo_vehiculo"]
        tipo_combustible_val = request.POST["tipo_combustible"]
        anio_modelo_val = request.POST["anio_modelo"]
        foto_val = request.FILES.get('foto')
        
        Vehiculo.objects.create(
            placa=placa_val,
            tipo_vehiculo=tipo_vehiculo_val,
            tipo_combustible=tipo_combustible_val,
            anio_modelo=int(anio_modelo_val),
            foto=foto_val
        )
        
        messages.success(request, 'Vehículo guardado exitosamente en la flota.') 
        return redirect('/listadodevehiculos/')
        
    return redirect('/listadodevehiculos/')

def listadodevehiculos(request):
    vehiculos = Vehiculo.objects.all() 
    return render(request, 'listadodevehiculos.html', {'vehiculos': vehiculos})

def editarVehiculo(request, id):
    vehiculo = Vehiculo.objects.get(id=id) 
    return render(request, 'editarVehiculo.html', {'vehiculo': vehiculo})

def actualizarVehiculo(request):
    if request.method == "POST":
        id_val = request.POST["id"]
        vehiculo = Vehiculo.objects.get(id=id_val)
        
        vehiculo.placa = request.POST["placa"]
        vehiculo.tipo_vehiculo = request.POST["tipo_vehiculo"]
        vehiculo.tipo_combustible = request.POST["tipo_combustible"]
        vehiculo.anio_modelo = request.POST["anio_modelo"]
        
        nueva_foto = request.FILES.get('foto')
        if nueva_foto: 
            # 1. Verificamos si ya existía una foto vieja asignada y si el archivo real existe en el disco
            if vehiculo.foto and os.path.isfile(vehiculo.foto.path):
                os.remove(vehiculo.foto.path) # 2. Borramos la foto anterior físicamente
            
            vehiculo.foto = nueva_foto
            
        vehiculo.save()
        messages.success(request, f"¡El vehículo {vehiculo.placa} ha sido actualizado correctamente!")
    return redirect('/listadodevehiculos/')

def eliminarVehiculo(request, id):
    vehiculo = Vehiculo.objects.get(id=id) 
    vehiculo.delete()
    messages.success(request, f"¡El vehículo {vehiculo.placa} ha sido eliminado de la flota correctamente!")
    return redirect('/listadodevehiculos/')

def NuevoMantenimiento(request):
    return render(request, 'NuevoMantenimiento.html')

def guardarMantenimiento(request):
    if request.method == "POST":
        Mantenimiento.objects.create(
            fecha_servicio=request.POST["fecha_servicio"],
            costo_taller=float(request.POST["costo_taller"]),
            tipo_mantenimiento=request.POST["tipo_mantenimiento"],
            repuestos_cambiados=request.POST["repuestos_cambiados"],
            pdf_diagnostico=request.FILES.get('pdf_diagnostico')
        )
        
        messages.success(request, 'Registro de taller/mantenimiento guardado con éxito.') 
        return redirect('/listadodemantenimientos/')
        
    return redirect('/listadodemantenimientos/')

def listadodemantenimientos(request):
    mantenimientos = Mantenimiento.objects.all() 
    return render(request, 'listadodemantenimientos.html', {'mantenimientos': mantenimientos})

def editarMantenimiento(request, id):
    mantenimiento = Mantenimiento.objects.get(id=id) 
    return render(request, 'editarMantenimiento.html', {'mantenimiento': mantenimiento})

def actualizarMantenimiento(request):
    if request.method == "POST":
        id_val = request.POST["id"]
        mantenimiento = Mantenimiento.objects.get(id=id_val)
        
        mantenimiento.fecha_servicio = request.POST["fecha_servicio"]
        mantenimiento.costo_taller = request.POST["costo_taller"]
        mantenimiento.tipo_mantenimiento = request.POST["tipo_mantenimiento"]
        mantenimiento.repuestos_cambiados = request.POST["repuestos_cambiados"]
        
        nuevo_pdf = request.FILES.get('pdf_diagnostico')
        if nuevo_pdf:
            if mantenimiento.pdf_diagnostico and os.path.isfile(mantenimiento.pdf_diagnostico.path):
                os.remove(mantenimiento.pdf_diagnostico.path) # 2. Borramos el archivo físico antiguo
                
            mantenimiento.pdf_diagnostico = nuevo_pdf
            
        mantenimiento.save()
        messages.success(request, f"¡El registro de mantenimiento ID {mantenimiento.id} ha sido actualizado correctamente!")
    return redirect('/listadodemantenimientos/')  

def eliminarMantenimiento(request, id):
    mantenimiento = Mantenimiento.objects.get(id=id) 
    mantenimiento.delete()
    messages.success(request, f"¡El registro de mantenimiento ID {mantenimiento.id} ha sido eliminado correctamente!")
    return redirect('/listadodemantenimientos/')