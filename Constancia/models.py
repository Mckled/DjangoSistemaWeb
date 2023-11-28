from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    Nombres_Completo = models.CharField(max_length=50)

    # Añadir campos personalizados según sea necesario

    objects = CustomUserManager()

    def __str__(self):
        return self.username

#==========================================================================================================#
#==========================================================================================================#

class Representante(models.Model):
    id_representante = models.AutoField(primary_key=True)
    Cedula_Representante = models.BigIntegerField()
    Nombres_Representante = models.CharField(max_length=50)
    Apellidos_Representante = models.CharField(max_length=50)
    Fecha_Nacimiento_Representante = models.DateField()
    GENERO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
    ]
    Genero_Representante = models.CharField(max_length=10, choices=GENERO_CHOICES)
    PARENTESCO_CHOICES = [
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Tio', 'Tio'),
        ('Tia', 'Tia'),
    ]
    Parentesco_Representante = models.CharField(max_length=10, choices=PARENTESCO_CHOICES)
    Lugar_Nacimiento_Representante = models.CharField(max_length=50)
    ENTIDAD_CHOICES = [
        ('Portuguesa', 'Portuguesa'),
        ('Barinas', 'Barinas'),
        ('Lara', 'Lara'),
        ('Caracas', 'Caracas'),
    ]
    Entidad_Federal_Representante = models.CharField(max_length=20, choices=ENTIDAD_CHOICES)
    Direccion_Habitacion_Representante = models.CharField(max_length=255)
    Telefono1_Representante = models.BigIntegerField()
    Telefono2_Representante = models.BigIntegerField(null=True, blank=True)
    Correo_Electronico_Representante = models.EmailField(unique=True, null=True, blank=True)
    Observacion_Representante = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.Cedula_Representante} {self.Nombres_Representante} {self.Apellidos_Representante}"

#==========================================================================================================#
#==========================================================================================================#

class Estudiante(models.Model):
    id_estudiante = models.AutoField(primary_key=True)
    Cedula_Estudiante = models.BigIntegerField()
    Nombres_Estudiante = models.CharField(max_length=50)
    Apellidos_Estudiante = models.CharField(max_length=50)
    Fecha_Nacimiento_Estudiante = models.DateField()
    GENERO_CHOICES = [
        ('Femenino', 'Femenino'),
        ('Masculino', 'Masculino'),
    ]
    Genero_Estudiante = models.CharField(max_length=10, choices=GENERO_CHOICES)
    Lugar_Nacimiento_Estudiante = models.CharField(max_length=50)
    ENTIDAD_CHOICES = [
        ('Portuguesa', 'Portuguesa'),
        ('Barinas', 'Barinas'),
        ('Lara', 'Lara'),
        ('Caracas', 'Caracas'),
    ]
    Entidad_Federal_Estudiante = models.CharField(max_length=20, choices=ENTIDAD_CHOICES)
    Fecha_Registro_Estudiante = models.DateField()
    Cedula_Representante = models.ForeignKey(Representante, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['Cedula_Estudiante']  # Añade la restricción UNIQUE

    def __str__(self):
        return f"{self.Cedula_Estudiante} {self.Nombres_Estudiante} {self.Apellidos_Estudiante}"
    
#==========================================================================================================#
#==========================================================================================================#

class Materia(models.Model):
    id_Materia = models.AutoField(primary_key=True)
    Nombre_Materia = models.CharField(max_length=50)

    class Meta:
        unique_together = ['Nombre_Materia']
    def __str__(self):
        return f"{self.Nombre_Materia}"

#==========================================================================================================#
#==========================================================================================================#

class Grado(models.Model):
    ID_Grado = models.AutoField(primary_key=True)
    ANO_GRADO_CHOICES = [
        ('Primero', 'Primero'),
        ('Segundo', 'Segundo'),
        ('Tercero', 'Tercero'),
        ('Cuarto', 'Cuarto'),
        ('Quinto', 'Quinto'),
    ]
    Ano_Grado = models.CharField(max_length=10, choices=ANO_GRADO_CHOICES)
    SECCION_GRADO_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    Seccion_Grado = models.CharField(max_length=1, choices=SECCION_GRADO_CHOICES)

    class Meta:
        unique_together = ['Ano_Grado', 'Seccion_Grado']
    
    def __str__(self):
        return f"{self.Ano_Grado} Sección {self.Seccion_Grado}"


#==========================================================================================================#
#==========================================================================================================#

class MateriaSeccion(models.Model):
    Id_Materia_Seccion = models.AutoField(primary_key=True)
    Materias = models.ManyToManyField(Materia, related_name='materias_all')
    Id_Grado = models.ForeignKey(Grado, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['Id_Grado']

    def get_materias_display_1(self):
        materias = [str(materia) for materia in self.Materias.all()]
        return f'({", ".join(materias)})'

    def __str__(self):
        return f"{self.Id_Grado}"

#==========================================================================================================#
#==========================================================================================================#

class Institucion(models.Model):
    id_Institucion =  models.AutoField(primary_key=True, unique=True)
    Codigo_Institucion = models.CharField(max_length=50)
    Nombre_Institucion = models.CharField(max_length=100)
    Ubicacion_Institucion = models.CharField(max_length=100)
    Correo_Institucion = models.EmailField(max_length=50)
    Telefono_Institucion = models.BigIntegerField()

    def __str__(self):
        return self.Nombre_Institucion

@receiver(post_save, sender=Institucion)
def limitar_un_registro(sender, instance, **kwargs):
    # Asegurarse de que solo haya un registro
    if Institucion.objects.count() > 1:
        instance.delete()

#==========================================================================================================#
#==========================================================================================================#

class Cargos(models.Model):
    id_cargos =  models.AutoField(primary_key=True)
    Cedula_Cargos = models.BigIntegerField()
    Nombres_Cargos = models.CharField(max_length=50)
    Apellidos_Cargos = models.CharField(max_length=50)
    Telefono_Cargos = models.BigIntegerField()
    Fecha_Ingreso_Cargos = models.DateField(null=True, blank=True)
    Fecha_Egreso_Cargos = models.DateField(null=True, blank=True)
    CARGO_CHOICES = [
        ('Director/a', 'Director/a'),
        ('Coordinador de control de estudios y evaluacion', 'Coordinador de control de estudios y evaluacion'),
    ]
    Cargo_Cargos = models.CharField(max_length=50, choices=CARGO_CHOICES)

    class Meta:
        unique_together = ['Cargo_Cargos']  # Añade la restricción UNIQUE

    def __str__(self):
        return f"{self.Nombres_Cargos} {self.Apellidos_Cargos} - {self.Cargo_Cargos}"

#==========================================================================================================#
#==========================================================================================================#

class InscripcionEstudiante(models.Model):
    id_Inscripcion_Estudiante = models.AutoField(primary_key=True)
    Cedula_Estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    CONDICION_CHOICES = [
        ('Regular', 'Regular'),
        ('Regular con materia pendiente', 'Regular con materia pendiente'),
        ('Repetiente', 'Repetiente'),
        ('Bachiller no cursante', 'Bachiller no cursante'),
    ]
    Condicion_Inscripcion = models.CharField(max_length=30, choices=CONDICION_CHOICES)
    Id_Materia_Seccion = models.ForeignKey(MateriaSeccion, on_delete=models.CASCADE)
    ANO_ESCOLAR_CHOICES = [
        ('2023-2024', '2023-2024'),
        ('2024-2025', '2024-2025'),
    ]
    Ano_Escolar = models.CharField(max_length=20, choices=ANO_ESCOLAR_CHOICES)
    id_cargos = models.ForeignKey(Cargos, on_delete=models.CASCADE)
    id_Institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    Fecha_Inscripcion = models.DateTimeField()

    def __str__(self):
        return f"Inscrito {self.id_Inscripcion_Estudiante} - {self.Cedula_Estudiante}"

#==========================================================================================================#
#==========================================================================================================#

class InscripcionMateriaBachillerNoCursante(models.Model):
    id_Inscripcion_Regular = models.AutoField(primary_key=True)
    id_Inscripcion_Estudiante = models.OneToOneField(InscripcionEstudiante, on_delete=models.CASCADE, unique=True)
    materias_pendientes = models.ManyToManyField(Materia, related_name='materias_pendientesX')

    def get_materias_display_2(self):
        materias = [str(materia) for materia in self.materias_pendientes.all()]
        return f'({", ".join(materias)})'

    def __str__(self):
        return f"Inscripción Materia Regular {self.id_Inscripcion_Regular} - {self.id_Inscripcion_Estudiante}"

#==========================================================================================================#
#==========================================================================================================#

class InscripcionMateriaRepitiente(models.Model):
    id_Inscripcion_Repitiente = models.AutoField(primary_key=True)
    id_Inscripcion_Estudiante = models.OneToOneField(InscripcionEstudiante, on_delete=models.CASCADE, unique=True)
    Materias_pendientes = models.ManyToManyField(Materia, related_name='materias_pendientes22')

    def get_materias_display_3(self):
        materias = [str(materia) for materia in self.Materias_pendientes.all()]
        return f'({", ".join(materias)})'

    def __str__(self):
        return f"Inscripción Materia Repitiente {self.id_Inscripcion_Repitiente} - {self.id_Inscripcion_Estudiante}"

#==========================================================================================================#
#==========================================================================================================#

class InscripcionMateriaPendiente(models.Model):
    id_Inscripcion_Pendiente = models.AutoField(primary_key=True)
    id_Inscripcion_Estudiante = models.OneToOneField(InscripcionEstudiante, on_delete=models.CASCADE, unique=True)
    materias_pendientes = models.ManyToManyField(Materia, related_name='materias_pendientes')
    Id_Grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='GRADO2')

    def get_materias_display_4(self):
        materias = [str(materia) for materia in self.materias_pendientes.all()]
        return f'({", ".join(materias)})'

    def __str__(self):
        return f"Inscripción Materia Pendiente {self.id_Inscripcion_Pendiente} - {self.id_Inscripcion_Estudiante}"



 