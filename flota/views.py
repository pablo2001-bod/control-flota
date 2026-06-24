import os
from django.shortcuts import render, redirect
from .models import Vehiculo, Mantenimiento
from django.contrib import messages 


def inicio(request):
    return render(request, 'inicio.html')

#Vehiculo

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
    # Capturar el ID
    # El primer parametro id es el de la BDD
    # El segundo es el que acompaña a request osea la variable
    vehiculoEliminado = Vehiculo.objects.get(id=id)
    
    # si el vehículo tiene foto y el archivo físico existe en el servidor
    # lo borramos
    # "os.path.exists"
    # Verifica si la foto realmente existe en la carpeta antes de hacer nada.
    # Evita que el sistema falle.
    if vehiculoEliminado.foto and os.path.exists(vehiculoEliminado.foto.path):
        # "os.remove"
        # Borra la foto físicamente del disco duro para que no ocupe espacio
        # innecesario (elimina la basura).
        os.remove(vehiculoEliminado.foto.path)
        
    vehiculoEliminado.delete()
    messages.success(request, 'Vehículo Eliminado Exitosamente')
    return redirect('/listadodevehiculos')

#Mantenimiento
 
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
    #Agrega esta línea para traer los vehículos
    vehiculos = Vehiculo.objects.all() 
    return render(request, 'editarMantenimiento.html', {
        'mantenimiento': mantenimiento,
        #Se los pasamos al HTML
        'vehiculos': vehiculos 
    })

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
    
    # SI EL MANTENIMIENTO TIENE PDF Y EL ARCHIVO FÍSICO EXISTE EN EL SERVIDOR LO BORRAMOS
    # "os.path.exists" Verifica si el PDF realmente existe en la carpeta antes de hacer nada.
    if mantenimiento.pdf_diagnostico and os.path.exists(mantenimiento.pdf_diagnostico.path):
        # "os.remove" Borra el PDF físicamente del disco duro para que no ocupe espacio innecesario.
        os.remove(mantenimiento.pdf_diagnostico.path)
        
    # Una vez borrado el archivo del disco duro, eliminamos el registro de la Base de Datos
    mantenimiento.delete()
    
    messages.success(request, f"¡El registro de mantenimiento ID {id} ha sido eliminado correctamente!")
    return redirect('/listadodemantenimientos/')