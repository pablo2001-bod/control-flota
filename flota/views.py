import os
from django.shortcuts import render, redirect
from .models import Vehiculo, Mantenimiento
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError  # Control de placas duplicadas

# --- SISTEMA DE AUTENTICACIÓN (LOGIN/LOGOUT) ---

def login_vista(request):
    mensaje = ""
    if request.method == 'POST':
        usuario_txt = request.POST.get('username')
        clave_txt = request.POST.get('password')
        user = authenticate(request, username=usuario_txt, password=clave_txt)
        if user is not None:
            login(request, user)
            return redirect('/')  # Redirige directo a la raíz del sistema
        else:
            mensaje = "Usuario o contraseña incorrectos."
            
    return render(request, 'login.html', {'mensaje': mensaje})

def logout_vista(request):
    logout(request)
    return redirect('login')


# --- VISTA DE INICIO (CON CONTROL DE ROLES) ---

@login_required(login_url='login')
def inicio(request):
    es_gerente = request.user.groups.filter(name='Gerente').exists()
    es_chofer = request.user.groups.filter(name='Chofer').exists()
    
    contexto = {
        'es_gerente': es_gerente,
        'es_chofer': es_chofer
    }
    return render(request, 'inicio.html', contexto)


# --- SECCIÓN VEHÍCULOS ---

@login_required(login_url='login')
def NuevoVehiculo(request):
    return render(request, 'NuevoVehiculo.html')

@login_required(login_url='login')
def guardarVehiculo(request):
    if request.method == "POST":
        placa_val = request.POST["placa"].strip().upper()
        tipo_vehiculo_val = request.POST["tipo_vehiculo"]
        tipo_combustible_val = request.POST["tipo_combustible"]
        anio_modelo_val = request.POST["anio_modelo"]
        seguro_vigente_val = 'seguro_vigente' in request.POST
        foto_val = request.FILES.get('foto')
        
        try:
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
        except IntegrityError:
            messages.error(request, f'Error: Ya existe un vehículo registrado con la placa {placa_val}.')
            return redirect('/NuevoVehiculo/')
            
    return redirect('/listadodevehiculos/')

@login_required(login_url='login')
def listadodevehiculos(request):
    es_gerente = request.user.groups.filter(name='Gerente').exists()
    es_chofer = request.user.groups.filter(name='Chofer').exists()
    
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
        'alertas': alertas_presupuesto,
        'es_gerente': es_gerente,
        'es_chofer': es_chofer
    })

@login_required(login_url='login')
def editarVehiculo(request, id):
    vehiculo = Vehiculo.objects.get(id=id) 
    return render(request, 'editarVehiculo.html', {'vehiculo': vehiculo})

@login_required(login_url='login')
def actualizarVehiculo(request):
    if request.method == "POST":
        id_val = request.POST["id"]
        vehiculo = Vehiculo.objects.get(id=id_val)
        
        vehiculo.placa = request.POST["placa"].strip().upper()
        vehiculo.tipo_vehiculo = request.POST["tipo_vehiculo"]
        vehiculo.tipo_combustible = request.POST["tipo_combustible"]
        vehiculo.anio_modelo = request.POST["anio_modelo"]
        vehiculo.seguro_vigente = 'seguro_vigente' in request.POST
        
        nueva_foto = request.FILES.get('foto')
        if nueva_foto: 
            # Corrección: Uso de os.path.exists para asegurar la eliminación física en el servidor
            if vehiculo.foto and os.path.exists(vehiculo.foto.path):
                try:
                    os.remove(vehiculo.foto.path) 
                except Exception:
                    pass
            vehiculo.foto = nueva_foto
            
        vehiculo.save()
        messages.success(request, f"¡El vehículo {vehiculo.placa} ha sido actualizado correctamente!")
    return redirect('/listadodevehiculos/')

@login_required(login_url='login')
def eliminarVehiculo(request, id):
    vehiculoEliminado = Vehiculo.objects.get(id=id)
    if vehiculoEliminado.foto and os.path.exists(vehiculoEliminado.foto.path):
        try:
            os.remove(vehiculoEliminado.foto.path)
        except Exception:
            pass
        
    vehiculoEliminado.delete()
    messages.success(request, 'Vehículo Eliminado Exitosamente')
    return redirect('/listadodevehiculos/')


# --- SECCIÓN MANTENIMIENTOS ---
 
@login_required(login_url='login')
def NuevoMantenimiento(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'NuevoMantenimiento.html', {'vehiculos': vehiculos})

@login_required(login_url='login')
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

@login_required(login_url='login')
def listadodemantenimientos(request):
    es_gerente = request.user.groups.filter(name='Gerente').exists()
    es_chofer = request.user.groups.filter(name='Chofer').exists()
    mantenimientos = Mantenimiento.objects.all() 
    return render(request, 'listadodemantenimientos.html', {
        'mantenimientos': mantenimientos,
        'es_gerente': es_gerente,
        'es_chofer': es_chofer
    })

@login_required(login_url='login')
def editarMantenimiento(request, id):
    mantenimiento = Mantenimiento.objects.get(id=id) 
    vehiculos = Vehiculo.objects.all() 
    return render(request, 'editarMantenimiento.html', {
        'mantenimiento': mantenimiento,
        'vehiculos': vehiculos 
    })

@login_required(login_url='login')
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
            # Corrección: Uso de os.path.exists para asegurar la eliminación física del PDF anterior
            if mantenimiento.pdf_diagnostico and os.path.exists(mantenimiento.pdf_diagnostico.path):
                try:
                    os.remove(mantenimiento.pdf_diagnostico.path)
                except Exception:
                    pass
            mantenimiento.pdf_diagnostico = nuevo_pdf
            
        mantenimiento.save()
        messages.success(request, f"¡El registro de mantenimiento ID {mantenimiento.id} ha sido actualizado correctamente!")
    return redirect('/listadodemantenimientos/')  

@login_required(login_url='login')
def eliminarMantenimiento(request, id):
    mantenimiento = Mantenimiento.objects.get(id=id)
    if mantenimiento.pdf_diagnostico and os.path.exists(mantenimiento.pdf_diagnostico.path):
        try:
            os.remove(mantenimiento.pdf_diagnostico.path)
        except Exception:
            pass
        
    mantenimiento.delete()
    messages.success(request, f"¡El registro de mantenimiento ID {id} ha sido eliminado correctamente!")
    return redirect('/listadodemantenimientos/')