from django.contrib.auth.models import Group
from Constancia.models import CustomUser

# Obtén los usuarios
usuario_super = CustomUser.objects.get(username='usuario_super')
usuario_regular = CustomUser.objects.get(username='usuario_regular')

# Obtén o crea los grupos
grupo_superuser, creado = Group.objects.get_or_create(name='Superuser')
grupo_usuarios, creado = Group.objects.get_or_create(name='Usuarios')

# Asigna usuarios a grupos
usuario_super.groups.add(grupo_superuser)
usuario_regular.groups.add(grupo_usuarios)


from django.contrib.auth.models import Permission
from Constancia.models import CustomUser

# Obtén los usuarios
usuario_super = CustomUser.objects.get(username='usuario_super')
usuario_regular = CustomUser.objects.get(username='usuario_regular')

# Obtén los permisos (puedes encontrar los permisos específicos en el panel de administración)
permiso_puede_hacer_algo = Permission.objects.get(codename='puede_hacer_algo')

# Asigna permisos a grupos
grupo_superuser.permissions.add(permiso_puede_hacer_algo)
grupo_usuarios.permissions.add(permiso_puede_hacer_algo)

