from django.urls import path
from flota import views

urlpatterns = [
    path('', views.inicio),
    
    # URLs de Vehículos
    path('NuevoVehiculo/', views.NuevoVehiculo),
    path('guardarVehiculo/', views.guardarVehiculo),
    path('listadodevehiculos/', views.listadodevehiculos),
    path('editarVehiculo/<int:id>/', views.editarVehiculo),
    path('actualizarVehiculo/', views.actualizarVehiculo),
    path('eliminarVehiculo/<int:id>/', views.eliminarVehiculo),
    
    # URLs de Mantenimientos
    path('NuevoMantenimiento/', views.NuevoMantenimiento),
    path('guardarMantenimiento/', views.guardarMantenimiento),
    path('listadodemantenimientos/', views.listadodemantenimientos),
    path('editarMantenimiento/<int:id>/', views.editarMantenimiento),
    path('actualizarMantenimiento/', views.actualizarMantenimiento),
    path('eliminarMantenimiento/<int:id>/', views.eliminarMantenimiento),
]