from django.shortcuts import render, redirect
from django.contrib import messages 
from .models import Vehiculo, Mantenimiento # Suponiendo que tus modelos se llaman así

# Ruta de inicio (Login o Dashboard)
def inicio(request):
    return render(request, 'index.html')

# --- CRUD VEHÍCULOS ---

def NuevoVehiculo(request):
    return render(request, 'NuevoVehiculo.html')

def guardarVehiculo(request):
    if request.method == "POST":
        placa = request.POST["placa"]
        tipo = request.POST["tipo_vehiculo"]
        combustible = request.POST["tipo_combustible"]
        seguro = request.POST.get("seguro", False) == "on" # Checkbox
        anio = request.POST["anio_modelo"]
        foto = request.FILES.get('foto')
        
        Vehiculo.objects.create(
            placa=placa,
            tipo_vehiculo=tipo,
            tipo_combustible=combustible,
            seguro_vigente=seguro,
            anio_modelo=int(anio),
            foto=foto
        )
        messages.success(request, 'Vehículo guardado exitosamente') 
        return redirect('/listadodevehiculos/')
    return redirect('/listadodevehiculos/')

def listadodevehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'listadodevehiculos.html', {'vehiculos': vehiculos})

def eliminarVehiculo(request, id):
    vehiculo = Vehiculo.objects.get(id=id) 
    vehiculo.delete()
    messages.success(request, f"¡Vehículo {vehiculo.placa} eliminado correctamente!")
    return redirect('/listadodevehiculos/')

def editarVehiculo(request, id):
    vehiculo = Vehiculo.objects.get(id=id) 
    return render(request, 'editarVehiculo.html', {'vehiculo': vehiculo})

def actualizarVehiculo(request):
    id = request.POST["id"]
    vehiculo = Vehiculo.objects.get(id=id)
    vehiculo.placa = request.POST["placa"]
    vehiculo.tipo_vehiculo = request.POST["tipo_vehiculo"]
    vehiculo.tipo_combustible = request.POST["tipo_combustible"]
    vehiculo.seguro_vigente = request.POST.get("seguro", False) == "on"
    vehiculo.anio_modelo = request.POST["anio_modelo"]
    if request.FILES.get('foto'):
        vehiculo.foto = request.FILES.get('foto')
    vehiculo.save()
    messages.success(request, f"¡Vehículo {vehiculo.placa} actualizado correctamente!")
    return redirect('/listadodevehiculos/')    

# --- CRUD MANTENIMIENTOS ---

def NuevoMantenimiento(request):
    return render(request, 'NuevoMantenimiento.html')

def guardarMantenimiento(request):
    if request.method == "POST":
        fecha = request.POST["fecha_servicio"]
        costo = request.POST["costo_taller"]
        tipo = request.POST["tipo_mantenimiento"]
        repuestos = request.POST["repuestos_cambiados"]
        pdf = request.FILES.get('pdf')
        
        Mantenimiento.objects.create(
            fecha_servicio=fecha,
            costo_taller=float(costo),
            tipo_mantenimiento=tipo,
            repuestos_cambiados=repuestos,
            pdf_diagnostico=pdf
        )
        messages.success(request, 'Mantenimiento registrado exitosamente') 
        return redirect('/listadodemantenimientos/')
    return redirect('/listadodemantenimientos/')

def listadodemantenimientos(request):
    mantenimientos = Mantenimiento.objects.all()
    return render(request, 'listadodemantenimientos.html', {'mantenimientos': mantenimientos})