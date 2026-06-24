import os
from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import Vehiculo, Mantenimiento

def inicio(request):
    return render(request, 'inicio.html')

# ==================== MÓDULO VEHÍCULOS ====================

def NuevoVehiculo(request):
    return render(request, 'NuevoVehiculo.html')

def guardarVehiculo(request):
    if request.method == "POST":
        placa_val = request.POST["placa"]
        tipo_vehiculo_val = request.POST["tipo_vehiculo"]
        tipo_combustible_val = request.POST["tipo_combustible"]
        anio_modelo_val = request.POST["anio_modelo"]
        seguro_vigente_val = 'seguro_vigente' in request.POST
        foto_val = request.FILES.get('foto')
        
        Vehiculo.objects.create(
            placa=placa_val,
            tipo_vehiculo=tipo_vehiculo_val,
            tipo_combustible=tipo_combustible_val,
            seguro_vigente=seguro_vigente_val,
            anio_modelo=int(anio_modelo_val),
            foto=foto_val
        )
        
        messages.success(request, 'Vehículo guardado exitosamente en la flota.') 
        return redirect('/listadodevehiculos/')
    return redirect('/listadodevehiculos/')

def listadodevehiculos(request):
    vehiculos_db = Vehiculo.objects.all()
    vehiculos_procesados = []
    alertas_presupuesto = []
    
    PRESUPUESTO_LIMITE_ANUAL = 1500.0
    
    for v in vehiculos_db:
        costo_acumulado = sum(m.costo_taller for m in v.mantenimientos.all())
        
        vehiculos_procesados.append({
            'id': v.id,
            'placa': v.placa,
            'tipo_vehiculo': v.tipo_vehiculo,
            'tipo_combustible': v.tipo_combustible,
            'seguro_vigente': v.seguro_vigente,
            'anio_modelo': v.anio_modelo,
            'foto': v.foto,
            'costo_acumulado': costo_acumulado
        })
        
        if costo_acumulado > PRESUPUESTO_LIMITE_ANUAL:
            alertas_presupuesto.append({
                'placa': v.placa,
                'costo': costo_acumulado,
                'exceso': costo_acumulado - PRESUPUESTO_LIMITE_ANUAL
            })
            
    return render(request, 'listadodevehiculos.html', {
        'vehiculos': vehiculos_procesados,
        'alertas': alertas_presupuesto
    })

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
        vehiculo.seguro_vigente = 'seguro_vigente' in request.POST
        
        nueva_foto = request.FILES.get('foto')
        if nueva_foto: 
            if vehiculo.foto and os.path.isfile(vehiculo.foto.path):
                os.remove(vehiculo.foto.path) 
            vehiculo.foto = nueva_foto
            
        vehiculo.save()
        messages.success(request, f"¡El vehículo {vehiculo.placa} ha sido actualizado correctamente!")
    return redirect('/listadodevehiculos/')

def eliminarVehiculo(request, id):
    vehiculo = Vehiculo.objects.get(id=id) 
    vehiculo.delete()
    messages.success(request, f"¡El vehículo {vehiculo.placa} ha sido eliminado de la flota correctamente!")
    return redirect('/listadodevehiculos/')


# ==================== MÓDULO MANTENIMIENTOS ====================

def NuevoMantenimiento(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'NuevoMantenimiento.html', {'vehiculos': vehiculos})

def guardarMantenimiento(request):
    if request.method == "POST":
        vehiculo_id = request.POST["vehiculo_id"]
        vehiculo_obj = Vehiculo.objects.get(id=vehiculo_id)
        
        Mantenimiento.objects.create(
            vehiculo=vehiculo_obj,
            fecha_servicio=request.POST["fecha_servicio"],
            costo_taller=float(request.POST["costo_taller"]),
            tipo_mantenimiento=request.POST["tipo_mantenimiento"],
            repuestos_cambiados=request.POST["repuestos_cambiados"],
            pdf_diagnostico=request.FILES.get('pdf_diagnostico')
        )
        
        messages.success(request, 'Registro de mantenimiento vehicular guardado con éxito.') 
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
        mantenimiento.costo_taller = float(request.POST["costo_taller"])
        mantenimiento.tipo_mantenimiento = request.POST["tipo_mantenimiento"]
        mantenimiento.repuestos_cambiados = request.POST["repuestos_cambiados"]
        
        nuevo_pdf = request.FILES.get('pdf_diagnostico')
        if nuevo_pdf:
            if mantenimiento.pdf_diagnostico and os.path.isfile(mantenimiento.pdf_diagnostico.path):
                os.remove(mantenimiento.pdf_diagnostico.path)
            mantenimiento.pdf_diagnostico = nuevo_pdf
            
        mantenimiento.save()
        messages.success(request, f"¡El registro de mantenimiento ID {mantenimiento.id} ha sido actualizado correctamente!")
    return redirect('/listadodemantenimientos/')  

def eliminarMantenimiento(request, id):
    mantenimiento = Mantenimiento.objects.get(id=id) 
    mantenimiento.delete()
    messages.success(request, f"¡El registro de mantenimiento ID {mantenimiento.id} ha sido eliminado correctamente!")
    return redirect('/listadodemantenimientos/')