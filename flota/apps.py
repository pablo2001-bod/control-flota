from django.apps import AppConfig
from django.db.models.signals import post_migrate

def crear_roles_y_usuarios_por_defecto(sender, **kwargs):
    # Importamos los modelos dentro de la función para evitar errores de carga
    from django.contrib.auth.models import Group, User
    
    # 1. Crear Grupos de Roles si no existen
    grupo_gerente, _ = Group.objects.get_or_create(name='Gerente')
    grupo_chofer, _ = Group.objects.get_or_create(name='Chofer')
    
    # 2. Crear un Chofer de prueba automático si no existe
    if not User.objects.filter(username='chofer1').exists():
        nuevo_chofer = User.objects.create_user(
            username='chofer1',
            password='chofer1234',
            first_name='Chofer',
            last_name='De Prueba'
        )
        # Lo metemos al grupo Chofer automáticamente
        nuevo_chofer.groups.add(grupo_chofer)
        print("🚀 Usuario 'chofer1' (Contraseña: chofer1234) creado con éxito.")

class FlotaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flota'

    def ready(self):
        # Cuando se ejecute o reconozca la app, corre la función de arriba
        post_migrate.connect(crear_roles_y_usuarios_por_defecto, sender=self)