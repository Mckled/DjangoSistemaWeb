from django.contrib import admin
from .models import Representante, Estudiante, InscripcionEstudiante, InscripcionMateriaBachillerNoCursante, InscripcionMateriaRepitiente, InscripcionMateriaPendiente, Materia, MateriaSeccion, Grado, Institucion, Cargos
# Register your models here.


@admin.register(Representante)
class RepresentanteAdmin(admin.ModelAdmin):
    list_display = ['Cedula_Representante', 'Nombres_Representante', 'Apellidos_Representante']
    


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['Cedula_Estudiante', 'Nombres_Estudiante', 'Apellidos_Estudiante']



@admin.register(InscripcionEstudiante)
class InscripcionEstudianteAdmin(admin.ModelAdmin):
    list_display = ['id_Inscripcion_Estudiante', 'Cedula_Estudiante', 'Condicion_Inscripcion']



class InscripcionMateriaBachillerNoCursanteAdmin(admin.ModelAdmin):
    list_display = ['id_Inscripcion_Regular', 'id_Inscripcion_Estudiante', 'get_materias']
    search_fields = ['id_Inscripcion_Regular', 'id_Inscripcion_Estudiante__Nombres_Estudiante', 'id_Inscripcion_Estudiante__Apellidos_Estudiante']

    def get_materias(self, obj):
        # Aquí construyes y devuelves la representación deseada de las materias
        materias = [f"Materia {i}: {getattr(obj, f'materia{i}')}" for i in range(1, 5) if getattr(obj, f'materia{i}')]
        return ", ".join(materias)

    get_materias.short_description = 'Materias'


admin.site.register(InscripcionMateriaBachillerNoCursante, InscripcionMateriaBachillerNoCursanteAdmin)


class InscripcionMateriaRepitienteAdmin(admin.ModelAdmin):
    list_display = ['id_Inscripcion_Repitiente', 'id_Inscripcion_Estudiante', 'get_materias']
    search_fields = ['id_Inscripcion_Repitiente', 'id_Inscripcion_Estudiante__Nombres_Estudiante', 'id_Inscripcion_Estudiante__Apellidos_Estudiante']


    def get_materias(self, obj):
        # Aquí construyes y devuelves la representación deseada de las materias
        materias = [f"Materia {i}: {getattr(obj, f'materia{i}')}" for i in range(1, 5) if getattr(obj, f'materia{i}')]
        return ", ".join(materias)

    get_materias.short_description = 'Materias'

admin.site.register(InscripcionMateriaRepitiente, InscripcionMateriaRepitienteAdmin)



class InscripcionMateriaPendienteAdmin(admin.ModelAdmin):
    list_display = ['id_Inscripcion_Pendiente', 'id_Inscripcion_Estudiante', 'get_materias', 'Id_Grado' ]
    search_fields = ['id_Inscripcion_Pendiente', 'id_Inscripcion_Estudiante__Nombres_Estudiante', 'id_Inscripcion_Estudiante__Apellidos_Estudiante']


    def get_materias(self, obj):
        # Aquí construyes y devuelves la representación deseada de las materias
        materias_pendientes= [f"{i}: {getattr(obj, f'materia{i}')}" for i in range(1, 3) if getattr(obj, f'materia{i}')]
        return ", ".join(materias_pendientes)

    get_materias.short_description = 'Materias Pendiente'

admin.site.register(InscripcionMateriaPendiente, InscripcionMateriaPendienteAdmin)



@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['id_Materia', 'Nombre_Materia']



@admin.register(MateriaSeccion)
class MateriaSeccionAdmin(admin.ModelAdmin):
    list_display = ['Id_Materia_Seccion', 'get_materias']

    def get_materias(self, obj):
        # Aquí construyes y devuelves la representación deseada de las materias
        Materias= [f"{i}: {getattr(obj, f'materia{i}')}" for i in range(1, 5) if getattr(obj, f'materia{i}')]
        return ", ".join(Materias)

    get_materias.short_description = 'Materias Pendiente'



@admin.register(Grado)
class GradoAdmin(admin.ModelAdmin):
    list_display = ['ID_Grado', 'Ano_Grado', 'Seccion_Grado']




@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ['Codigo_Institucion', 'Nombre_Institucion', 'Ubicacion_Institucion']



@admin.register(Cargos)
class CargosAdmin(admin.ModelAdmin):
    list_display = ['Cedula_Cargos', 'Nombres_Cargos', 'Apellidos_Cargos', 'Cargo_Cargos']


#@admin.register(InscripcionEstudiante)
#class InscripcionEstudianteAdmin(admin.ModelAdmin):
    #list_display = ['id_inscripcion', 'cedula_estudiante', 'condicion', 'id_Grado', 'ano_escolar', 'cedula_cargos', 'codigo_inst', 'fecha_inscripcion']
    #list_filter = ('condicion', 'ano_escolar' )
    #search_fields = ('Cedula_estudiante', 'Condicion', 'id_Grado', 'Ano_escolar', 'Fecha_inscripcion')

