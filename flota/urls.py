# Archivo para gestionar las rutas internas de la aplicacion flota
from django.urls import path
# Importamos la lógica de negocio de la aplicación
from . import views

# Listado de rutas de la Aplicación
urlpatterns = [
    path('', views.inicio),
    
    # Rutas Vehículos
    path('NuevoVehiculo/', views.NuevoVehiculo),
    path('guardarVehiculo/', views.guardarVehiculo),
    path('listadodevehiculos/', views.listadodevehiculos),
    path('eliminarVehiculo/<int:id>/', views.eliminarVehiculo, name='eliminarVehiculo'),
    path('editarVehiculo/<int:id>/', views.editarVehiculo, name='editarVehiculo'),
    path('actualizarVehiculo/', views.actualizarVehiculo, name='actualizarVehiculo'),
    
    # Rutas Mantenimientos
    path('NuevoMantenimiento/', views.NuevoMantenimiento),
    path('guardarMantenimiento/', views.guardarMantenimiento),
    path('listadodemantenimientos/', views.listadodemantenimientos),
]