# urls.py
from django.urls import path
from . import views

# urls.py



from django.contrib.auth import views as auth_views

urlpatterns = [
    #inicio
    path('', views.login_user, name='login_user'),
    path('index/', views.EstadisticasEstudiantesView.as_view(), name='index'),
    path('estadisticas_estudiantes/', views.EstadisticasEstudiantesView.as_view(), name='estadisticas_estudiantes'),
    #Usario
    path('register_user/', views.register_user, name='register_user'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    #
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    #Representante
    path('agregar_representante/', views.AgregarRepresentanteView.as_view(), name='agregar_representante'),
    path('editar_representante/<int:cedula_representante>/', views.EditarRepresentanteView.as_view(), name='editar_representante'),
    path('eliminar_representante/<int:cedula_representante>/', views.EliminarRepresentanteView.as_view(), name='eliminar_representante'),
    path('lista_representantes/', views.ListaRepresentantesView.as_view(), name='lista_representantes'),
    #Estudiante
    path('agregar_estudiante/', views.AgregarEstudianteView.as_view(), name='agregar_estudiante'),
    path('editar_estudiante/<int:cedula_estudiante>/', views.EditarEstudianteView.as_view(), name='editar_estudiante'),
    path('eliminar_estudiante/<int:cedula_estudiante>/', views.EliminarEstudianteView.as_view(), name='eliminar_estudiante'),
    path('lista_estudiantes/', views.ListaEstudiantesView.as_view(), name='lista_estudiantes'),
    #Materias
    path('agregar_materia/', views.AgregarMateriaView.as_view(), name='agregar_materia'),
    path('editar_materia/<int:id_materia>/', views.EditarMateriaView.as_view(), name='editar_materia'),
    path('eliminar_materia/<int:id_materia>/', views.EliminarMateriaView.as_view(), name='eliminar_materia'),
    path('lista_materias/', views.ListaMateriasView.as_view(), name='lista_materias'),
    #GRADO
    path('agregar_grado/', views.AgregarGradoView.as_view(), name='agregar_grado'),
    path('editar_grado/<int:id_grado>/', views.EditarGradoView.as_view(), name='editar_grado'),
    path('eliminar_grado/<int:id_grado>/', views.EliminarGradoView.as_view(), name='eliminar_grado'),
    path('lista_grados/', views.ListaGradosView.as_view(), name='lista_grados'),
    #MateriaSeccion
    path('agregar_materia_seccion/', views.AgregarMateriaSeccionView.as_view(), name='agregar_materia_seccion'),
    path('editar_materia_seccion/<int:id_materia_seccion>/', views.EditarMateriaSeccionView.as_view(), name='editar_materia_seccion'),
    path('eliminar_materia_seccion/<int:id_materia_seccion>/', views.EliminarMateriaSeccionView.as_view(), name='eliminar_materia_seccion'),
    path('lista_materias_seccion/', views.ListaMateriasSeccionView.as_view(), name='lista_materias_seccion'),
    #INSTITUCION
    path('agregar_institucion/', views.AgregarInstitucionView.as_view(), name='agregar_institucion'),
    path('editar_institucion/<str:codigo_institucion>/', views.EditarInstitucionView.as_view(), name='editar_institucion'),
    path('eliminar_institucion/<str:codigo_institucion>/', views.EliminarInstitucionView.as_view(), name='eliminar_institucion'),
    path('lista_instituciones/', views.ListaInstitucionesView.as_view(), name='lista_instituciones'),
    #cargos
    path('agregar_jefe/', views.AgregarJefeView.as_view(), name='agregar_jefe'),
    path('editar_jefe/<str:cedula_cargos>/', views.EditarJefeView.as_view(), name='editar_jefe'),
    path('eliminar_jefe/<str:cedula_cargos>/', views.EliminarJefeView.as_view(), name='eliminar_jefe'),
    path('lista_jefes/', views.ListaJefesView.as_view(), name='lista_jefes'),
    #InscripcionEstudiante
    path('agregar_inscripcion_estudiante/', views.AgregarInscripcionEstudianteView.as_view(), name='agregar_inscripcion_estudiante'),
    path('editar_inscripcion_estudiante/<int:id_inscripcion>/', views.EditarInscripcionEstudianteView.as_view(), name='editar_inscripcion_estudiante'),
    path('eliminar_inscripcion_estudiante/<int:id_inscripcion>/', views.EliminarInscripcionEstudianteView.as_view(), name='eliminar_inscripcion_estudiante'),
    path('lista_inscripciones_estudiantes/', views.ListaInscripcionesEstudiantesView.as_view(), name='lista_inscripciones_estudiantes'),
    #InscripcionEstudianteRegular
    path('agregar_inscripcion_materia_regular/', views.AgregarInscripcionMateriaRegularView.as_view(), name='agregar_inscripcion_materia_regular'),
    path('editar_inscripcion_materia_regular/<int:id_inscripcion_regular>/', views.EditarInscripcionMateriaRegularView.as_view(), name='editar_inscripcion_materia_regular'),
    path('eliminar_inscripcion_materia_regular/<int:id_inscripcion_regular>/', views.EliminarInscripcionMateriaRegularView.as_view(), name='eliminar_inscripcion_materia_regular'),
    path('inscripcion_materia_regular_lista/', views.InscripcionMateriaRegularListaView.as_view(), name='inscripcion_materia_regular_lista'),
    #InscripcionEstudianteMateriaPendiente
    path('agregar_inscripcion_materia_pendiente/', views.AgregarInscripcionMateriaPendienteView.as_view(), name='agregar_inscripcion_materia_pendiente'),
    path('editar_inscripcion_materia_pendiente/<int:id_inscripcion_pendiente>/', views.EditarInscripcionMateriaPendienteView.as_view(), name='editar_inscripcion_materia_pendiente'),
    path('eliminar_inscripcion_materia_pendiente/<int:id_inscripcion_pendiente>/', views.EliminarInscripcionMateriaPendienteView.as_view(), name='eliminar_inscripcion_materia_pendiente'),
    path('lista_inscripciones_materias_pendientes/', views.ListaInscripcionesMateriasPendientesView.as_view(), name='lista_inscripciones_materias_pendientes'),
    #InscripcionEstudianteMateria
    path('agregar_inscripcion_materia_repitiente/', views.AgregarInscripcionMateriaRepitienteView.as_view(), name='agregar_inscripcion_materia_repitiente'),
    path('editar_inscripcion_materia_repitiente/<int:id_inscripcion_repitiente>/', views.EditarInscripcionMateriaRepitienteView.as_view(), name='editar_inscripcion_materia_repitiente'),
    path('eliminar_inscripcion_materia_repitiente/<int:id_inscripcion_repitiente>/', views.EliminarInscripcionMateriaRepitienteView.as_view(), name='eliminar_inscripcion_materia_repitiente'),
    path('lista_inscripciones_materias_repitientes/', views.ListaInscripcionesMateriasRepitientesView.as_view(), name='lista_inscripciones_materias_repitientes'),
    #constancia
    path('generar_constancia_estudios/<int:cedula_estudiante>/', views.generar_constancia_estudios, name='generar_constancia_estudios'),
    path('generar_informacion_alumno/<str:cedula_estudiante>/', views.generar_informacion_alumno, name='generar_informacion_alumno'),
    path('generar_informe_estudiantes/', views.generar_informe_estudiantes, name='generar_informe_estudiantes'),
    path('generar_informe_inscripcion/', views.generar_informe_inscripcion, name='generar_informe_inscripcion'),
]