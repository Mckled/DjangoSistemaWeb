from django.shortcuts import render, redirect, get_object_or_404
from .models import Representante, Estudiante, InscripcionEstudiante, InscripcionMateriaBachillerNoCursante, InscripcionMateriaRepitiente, InscripcionMateriaPendiente, Materia, MateriaSeccion, Grado, Institucion, Cargos, CustomUser
from .forms import RepresentanteForm, EstudianteForm, InscripcionEstudianteForm, InscripcionMateriaRepitienteForm, InscripcionMateriaBachillerNoCursanteForm, InscripcionMateriaPendienteForm, MateriaForm, MateriaSeccionForm, GradoForm, InstitucionForm, CargosForm, CustomUserCreationForm, CustomAuthenticationForm, CustomUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from .models import CustomUser
from django.contrib import messages
from django.db.models import Q
#=======================================================================================================#
#=======================================================================================================#
#pagina de incio

class IndexView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    template_name = 'index.html'  # Especifica el nombre de la plantilla que estás utilizando

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        estudiantes = Estudiante.objects.all()

        if query:
            estudiantes = estudiantes.filter(
                Q(Cedula_Estudiante__icontains=query)
            )

        return render(request, self.template_name, {'estudiantes': estudiantes})
#=======================================================================================================#
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import Group

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            is_superuser = form.cleaned_data.get('is_superuser')
            if is_superuser:
                user.is_staff = True
                user.is_superuser = True
            user.save()
             # Asigna usuarios a grupos
            if is_superuser:
                # Si es superusuario, puedes asignarlo a un grupo específico (opcional)
                group_name = 'usersuper'
            else:
                # Si no es superusuario, asigna a otro grupo con permisos específicos
                group_name = 'usersimple'

            # Obtén el nombre del grupo desde el formulario (puedes ajustar esto según tu lógica)
            group_name = form.cleaned_data.get('group_name', 'Usuarios')

            # Asegúrate de que el grupo exista
            group, created = Group.objects.get_or_create(name=group_name)

            # Asigna el usuario al grupo
            user.groups.add(group)

            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('login_user')

    else:
        form = CustomUserCreationForm()
    return render(request, 'register_user.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('index')  # Reemplaza 'dashboard' con la URL a la que deseas redirigir después del inicio de sesión
            else:
                # Agregar mensaje de error al formulario
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login_user.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Cierre de sesión exitoso.')
    return redirect('login_user')  # Reemplaza 'login' con la URL a la que deseas redirigir después del cierre de sesión



@login_required
def view_profile(request):
    user = request.user
    return render(request, 'view_profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('login_user')  # Cierra sesión después de eliminar el perfil
    return render(request, 'delete_profile.html', {'user': user})
#=======================================================================================================#
#REPRESENTANTE
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect


class AgregarRepresentanteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = RepresentanteForm()
        return render(request, 'agregar_representante.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RepresentanteForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_representantes')
        return render(request, 'agregar_representante.html', {'form': form})

class EditarRepresentanteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, cedula_representante, *args, **kwargs):
        representante = get_object_or_404(Representante, Cedula_Representante=cedula_representante)
        form = RepresentanteForm(instance=representante)
        return render(request, 'editar_representante.html', {'form': form, 'representante': representante})

    def post(self, request, cedula_representante, *args, **kwargs):
        representante = get_object_or_404(Representante, Cedula_Representante=cedula_representante)
        form = RepresentanteForm(request.POST, instance=representante)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_representantes')
        return render(request, 'editar_representante.html', {'form': form, 'representante': representante})

class EliminarRepresentanteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, cedula_representante, *args, **kwargs):
        representante = get_object_or_404(Representante, Cedula_Representante=cedula_representante)
        messages.success(request, "Eliminado correctamente")
        representante.delete()
        return redirect('lista_representantes')

    def get(self, request, cedula_representante, *args, **kwargs):
        representante = get_object_or_404(Representante, Cedula_Representante=cedula_representante)
        return render(request, 'eliminar_representante.html', {'representante': representante})

class ListaRepresentantesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        representantes = Representante.objects.all()
        return render(request, 'lista_representantes.html', {'representantes': representantes})

#=======================================================================================================#
#=======================================================================================================#
#ESTUDIANTE

class AgregarEstudianteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = EstudianteForm()
        return render(request, 'agregar_estudiante.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EstudianteForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_estudiantes')
        return render(request, 'agregar_estudiante.html', {'form': form})

class EditarEstudianteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, cedula_estudiante, *args, **kwargs):
        estudiante = get_object_or_404(Estudiante, Cedula_Estudiante=cedula_estudiante)
        form = EstudianteForm(instance=estudiante)
        return render(request, 'editar_estudiante.html', {'form': form, 'estudiante': estudiante})

    def post(self, request, cedula_estudiante, *args, **kwargs):
        estudiante = get_object_or_404(Estudiante, Cedula_Estudiante=cedula_estudiante)
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_estudiantes')
        return render(request, 'editar_estudiante.html', {'form': form, 'estudiante': estudiante})

class EliminarEstudianteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, cedula_estudiante, *args, **kwargs):
        estudiante = get_object_or_404(Estudiante, Cedula_Estudiante=cedula_estudiante)
        messages.success(request, "Eliminado correctamente")
        estudiante.delete()
        return redirect('lista_estudiantes')

    def get(self, request, cedula_estudiante, *args, **kwargs):
        estudiante = get_object_or_404(Estudiante, Cedula_Estudiante=cedula_estudiante)
        return render(request, 'eliminar_estudiante.html', {'estudiante': estudiante})

class ListaEstudiantesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        estudiantes = Estudiante.objects.all()
        return render(request, 'lista_estudiantes.html', {'estudiantes': estudiantes})

#=======================================================================================================#
#=======================================================================================================#
#MATERIA

class AgregarMateriaView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = MateriaForm()
        return render(request, 'agregar_materia.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MateriaForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente") 
            form.save()
            return redirect('lista_materias')
        return render(request, 'agregar_materia.html', {'form': form})

class EditarMateriaView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, id_materia, *args, **kwargs):
        materia = get_object_or_404(Materia, id_Materia=id_materia)
        form = MateriaForm(instance=materia)
        return render(request, 'editar_materia.html', {'form': form, 'materia': materia})

    def post(self, request, id_materia, *args, **kwargs):
        materia = get_object_or_404(Materia, id_Materia=id_materia)
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_materias')
        return render(request, 'editar_materia.html', {'form': form, 'materia': materia})

class EliminarMateriaView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, id_materia, *args, **kwargs):
        materia = get_object_or_404(Materia, id_Materia=id_materia)
        messages.success(request, "Eliminado correctamente")
        materia.delete() 
        return redirect('lista_materias')

    def get(self, request, id_materia, *args, **kwargs):
        materia = get_object_or_404(Materia, id_Materia=id_materia)
        return render(request, 'eliminar_materia.html', {'materia': materia})

class ListaMateriasView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        materias = Materia.objects.all()
        return render(request, 'lista_materias.html', {'materias': materias})

#=======================================================================================================#
#=======================================================================================================#
#GRADO

class AgregarGradoView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = GradoForm()
        return render(request, 'agregar_grado.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = GradoForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_grados')
        return render(request, 'agregar_grado.html', {'form': form})

class EditarGradoView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, id_grado, *args, **kwargs):
        grado = get_object_or_404(Grado, ID_Grado=id_grado)
        form = GradoForm(instance=grado)
        return render(request, 'editar_grado.html', {'form': form, 'grado': grado})

    def post(self, request, id_grado, *args, **kwargs):
        grado = get_object_or_404(Grado, ID_Grado=id_grado)
        form = GradoForm(request.POST, instance=grado)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_grados')
        return render(request, 'editar_grado.html', {'form': form, 'grado': grado})

class EliminarGradoView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, id_grado, *args, **kwargs):
        grado = get_object_or_404(Grado, ID_Grado=id_grado)
        messages.success(request, "Eliminado correctamente")
        grado.delete()
        return redirect('lista_grados')

    def get(self, request, id_grado, *args, **kwargs):
        grado = get_object_or_404(Grado, ID_Grado=id_grado)
        return render(request, 'eliminar_grado.html', {'grado': grado})

class ListaGradosView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        grados = Grado.objects.all()
        return render(request, 'lista_grados.html', {'grados': grados})

#=======================================================================================================#
#=======================================================================================================#
#MateriaSeccion

class AgregarMateriaSeccionView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = MateriaSeccionForm()
        return render(request, 'agregar_materia_seccion.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = MateriaSeccionForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_materias_seccion')
        return render(request, 'agregar_materia_seccion.html', {'form': form})

class EditarMateriaSeccionView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, id_materia_seccion, *args, **kwargs):
        materia_seccion = get_object_or_404(MateriaSeccion, Id_Materia_Seccion=id_materia_seccion)
        form = MateriaSeccionForm(instance=materia_seccion)
        return render(request, 'editar_materia_seccion.html', {'form': form, 'materia_seccion': materia_seccion})

    def post(self, request, id_materia_seccion, *args, **kwargs):
        materia_seccion = get_object_or_404(MateriaSeccion, Id_Materia_Seccion=id_materia_seccion)
        form = MateriaSeccionForm(request.POST, instance=materia_seccion)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_materias_seccion')
        return render(request, 'editar_materia_seccion.html', {'form': form, 'materia_seccion': materia_seccion})

class EliminarMateriaSeccionView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, id_materia_seccion, *args, **kwargs):
        materia_seccion = get_object_or_404(MateriaSeccion, Id_Materia_Seccion=id_materia_seccion)
        messages.success(request, "Eliminado correctamente")
        materia_seccion.delete()
        return redirect('lista_materias_seccion')

    def get(self, request, id_materia_seccion, *args, **kwargs):
        materia_seccion = get_object_or_404(MateriaSeccion, Id_Materia_Seccion=id_materia_seccion)
        return render(request, 'eliminar_materia_seccion.html', {'materia_seccion': materia_seccion})

class ListaMateriasSeccionView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        materias_seccion = MateriaSeccion.objects.all()
        return render(request, 'lista_materias_seccion.html', {'materias_seccion': materias_seccion})
#=======================================================================================================#
#=======================================================================================================#
#INSTITUCION

class AgregarInstitucionView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = InstitucionForm()
        return render(request, 'agregar_institucion.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = InstitucionForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_instituciones')
        return render(request, 'agregar_institucion.html', {'form': form})

class EditarInstitucionView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, codigo_institucion, *args, **kwargs):
        institucion = get_object_or_404(Institucion, Codigo_Institucion=codigo_institucion)
        form = InstitucionForm(instance=institucion)
        return render(request, 'editar_institucion.html', {'form': form, 'institucion': institucion})

    def post(self, request, codigo_institucion, *args, **kwargs):
        institucion = get_object_or_404(Institucion, Codigo_Institucion=codigo_institucion)
        form = InstitucionForm(request.POST, instance=institucion)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_instituciones')
        return render(request, 'editar_institucion.html', {'form': form, 'institucion': institucion})

class EliminarInstitucionView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, codigo_institucion, *args, **kwargs):
        institucion = get_object_or_404(Institucion, Codigo_Institucion=codigo_institucion)
        messages.success(request, "Eliminado correctamente")
        institucion.delete()
        return redirect('lista_instituciones')

    def get(self, request, codigo_institucion, *args, **kwargs):
        institucion = get_object_or_404(Institucion, Codigo_Institucion=codigo_institucion)
        return render(request, 'eliminar_institucion.html', {'institucion': institucion})

class ListaInstitucionesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        instituciones = Institucion.objects.all()
        return render(request, 'lista_instituciones.html', {'instituciones': instituciones})

#=======================================================================================================#
#=======================================================================================================#
#Jefe

class AgregarJefeView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = CargosForm()
        return render(request, 'agregar_jefe.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CargosForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_jefes')
        return render(request, 'agregar_jefe.html', {'form': form})

class EditarJefeView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, cedula_cargos, *args, **kwargs):
        jefe = get_object_or_404(Cargos, id_cargos=cedula_cargos)
        form = CargosForm(instance=jefe)
        return render(request, 'editar_jefe.html', {'form': form, 'jefe': jefe})

    def post(self, request, cedula_cargos, *args, **kwargs):
        jefe = get_object_or_404(Cargos, id_cargos=cedula_cargos)
        form = CargosForm(request.POST, instance=jefe)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_jefes')
        return render(request, 'editar_jefe.html', {'form': form, 'jefe': jefe})

class EliminarJefeView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, cedula_cargos, *args, **kwargs):
        jefe = get_object_or_404(Cargos, id_cargos=cedula_cargos)
        messages.success(request, "Eliminado correctamente")
        jefe.delete()
        return redirect('lista_jefes')

    def get(self, request, cedula_cargos, *args, **kwargs):
        jefe = get_object_or_404(Cargos, id_cargos=cedula_cargos)
        return render(request, 'eliminar_jefe.html', {'jefe': jefe})

class ListaJefesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        jefes = Cargos.objects.all()
        return render(request, 'lista_jefes.html', {'jefes': jefes})
#=======================================================================================================#
#=======================================================================================================#
#INCRIPCION

class AgregarInscripcionEstudianteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = InscripcionEstudianteForm()
        return render(request, 'agregar_inscripcion_estudiante.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = InscripcionEstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Agregado correctamente")
            return redirect('lista_inscripciones_estudiantes')
        return render(request, 'agregar_inscripcion_estudiante.html', {'form': form})

class EditarInscripcionEstudianteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, id_inscripcion, *args, **kwargs):
        inscripcion_estudiante = get_object_or_404(InscripcionEstudiante, id_Inscripcion_Estudiante=id_inscripcion)
        form = InscripcionEstudianteForm(instance=inscripcion_estudiante)
        return render(request, 'editar_inscripcion_estudiante.html', {'form': form, 'inscripcion_estudiante': inscripcion_estudiante})

    def post(self, request, id_inscripcion, *args, **kwargs):
        inscripcion_estudiante = get_object_or_404(InscripcionEstudiante, id_Inscripcion_Estudiante=id_inscripcion)
        form = InscripcionEstudianteForm(request.POST, instance=inscripcion_estudiante)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_inscripciones_estudiantes')
        return render(request, 'editar_inscripcion_estudiante.html', {'form': form, 'inscripcion_estudiante': inscripcion_estudiante})

class EliminarInscripcionEstudianteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, id_inscripcion, *args, **kwargs):
        inscripcion_estudiante = get_object_or_404(InscripcionEstudiante, id_Inscripcion_Estudiante=id_inscripcion)
        messages.success(request, "Eliminado correctamente")
        inscripcion_estudiante.delete()
        return redirect('lista_inscripciones_estudiantes')

    def get(self, request, id_inscripcion, *args, **kwargs):
        inscripcion_estudiante = get_object_or_404(InscripcionEstudiante, id_Inscripcion_Estudiante=id_inscripcion)
        return render(request, 'eliminar_inscripcion_estudiante.html', {'inscripcion_estudiante': inscripcion_estudiante})

class ListaInscripcionesEstudiantesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        inscripciones_estudiantes = InscripcionEstudiante.objects.all()
        return render(request, 'lista_inscripciones_estudiantes.html', {'inscripciones_estudiantes': inscripciones_estudiantes})

#=======================================================================================================#
#=======================================================================================================#
#InscripcionMateriaRegular

class InscripcionMateriaRegularListaView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        inscripciones_materia_regular = InscripcionMateriaBachillerNoCursante.objects.all()
        return render(request, 'inscripcion_materia_regular_lista.html', {'inscripciones_materia_regular': inscripciones_materia_regular})

class AgregarInscripcionMateriaRegularView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = InscripcionMateriaBachillerNoCursanteForm()
        return render(request, 'agregar_inscripcion_materia_regular.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = InscripcionMateriaBachillerNoCursanteForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('inscripcion_materia_regular_lista')
        return render(request, 'agregar_inscripcion_materia_regular.html', {'form': form})

class EditarInscripcionMateriaRegularView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, id_inscripcion_regular, *args, **kwargs):
        inscripcion_materia_regular = get_object_or_404(InscripcionMateriaBachillerNoCursante, id_Inscripcion_Regular=id_inscripcion_regular)
        form = InscripcionMateriaBachillerNoCursanteForm(instance=inscripcion_materia_regular)
        return render(request, 'editar_inscripcion_materia_regular.html', {'form': form, 'inscripcion_materia_regular': inscripcion_materia_regular})

    def post(self, request, id_inscripcion_regular, *args, **kwargs):
        inscripcion_materia_regular = get_object_or_404(InscripcionMateriaBachillerNoCursante, id_Inscripcion_Regular=id_inscripcion_regular)
        form = InscripcionMateriaBachillerNoCursanteForm(request.POST, instance=inscripcion_materia_regular)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('inscripcion_materia_regular_lista')
        return render(request, 'editar_inscripcion_materia_regular.html', {'form': form, 'inscripcion_materia_regular': inscripcion_materia_regular})

class EliminarInscripcionMateriaRegularView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, id_inscripcion_regular, *args, **kwargs):
        inscripcion_materia_regular = get_object_or_404(InscripcionMateriaBachillerNoCursante, id_Inscripcion_Regular=id_inscripcion_regular)
        messages.success(request, "Eliminado correctamente")
        inscripcion_materia_regular.delete()
        return redirect('inscripcion_materia_regular_lista')

    def get(self, request, id_inscripcion_regular, *args, **kwargs):
        inscripcion_materia_regular = get_object_or_404(InscripcionMateriaBachillerNoCursante, id_Inscripcion_Regular=id_inscripcion_regular)
        return render(request, 'eliminar_inscripcion_materia_regular.html', {'inscripcion_materia_regular': inscripcion_materia_regular})

#=======================================================================================================#
#=======================================================================================================#
#InscripcionMateriaRegular

class AgregarInscripcionMateriaPendienteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = InscripcionMateriaPendienteForm()
        return render(request, 'agregar_inscripcion_materia_pendiente.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = InscripcionMateriaPendienteForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_inscripciones_materias_pendientes')
        return render(request, 'agregar_inscripcion_materia_pendiente.html', {'form': form})

class EditarInscripcionMateriaPendienteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, id_inscripcion_pendiente, *args, **kwargs):
        inscripcion_materia_pendiente = get_object_or_404(InscripcionMateriaPendiente, id_Inscripcion_Pendiente=id_inscripcion_pendiente)
        form = InscripcionMateriaPendienteForm(instance=inscripcion_materia_pendiente)
        return render(request, 'editar_inscripcion_materia_pendiente.html', {'form': form, 'inscripcion_materia_pendiente': inscripcion_materia_pendiente})

    def post(self, request, id_inscripcion_pendiente, *args, **kwargs):
        inscripcion_materia_pendiente = get_object_or_404(InscripcionMateriaPendiente, id_Inscripcion_Pendiente=id_inscripcion_pendiente)
        form = InscripcionMateriaPendienteForm(request.POST, instance=inscripcion_materia_pendiente)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_inscripciones_materias_pendientes')
        return render(request, 'editar_inscripcion_materia_pendiente.html', {'form': form, 'inscripcion_materia_pendiente': inscripcion_materia_pendiente})

class EliminarInscripcionMateriaPendienteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, id_inscripcion_pendiente, *args, **kwargs):
        inscripcion_materia_pendiente = get_object_or_404(InscripcionMateriaPendiente, id_Inscripcion_Pendiente=id_inscripcion_pendiente)
        messages.success(request, "Eliminado correctamente")
        inscripcion_materia_pendiente.delete()
        return redirect('lista_inscripciones_materias_pendientes')

    def get(self, request, id_inscripcion_pendiente, *args, **kwargs):
        inscripcion_materia_pendiente = get_object_or_404(InscripcionMateriaPendiente, id_Inscripcion_Pendiente=id_inscripcion_pendiente)
        return render(request, 'eliminar_inscripcion_materia_pendiente.html', {'inscripcion_materia_pendiente': inscripcion_materia_pendiente})

class ListaInscripcionesMateriasPendientesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        inscripciones_materias_pendientes = InscripcionMateriaPendiente.objects.all()
        return render(request, 'lista_inscripciones_materias_pendientes.html', {'inscripciones_materias_pendientes': inscripciones_materias_pendientes})

#=======================================================================================================#
#=======================================================================================================#
#InscripcionMateriaReptitiente

class AgregarInscripcionMateriaRepitienteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        form = InscripcionMateriaRepitienteForm()
        return render(request, 'agregar_inscripcion_materia_repitiente.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = InscripcionMateriaRepitienteForm(request.POST)
        if form.is_valid():
            messages.success(request, "Agregado correctamente")
            form.save()
            return redirect('lista_inscripciones_materias_repitientes')
        return render(request, 'agregar_inscripcion_materia_repitiente.html', {'form': form})

class EditarInscripcionMateriaRepitienteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, id_inscripcion_repitiente, *args, **kwargs):
        inscripcion_materia_repitiente = get_object_or_404(InscripcionMateriaRepitiente, id_Inscripcion_Repitiente=id_inscripcion_repitiente)
        form = InscripcionMateriaRepitienteForm(instance=inscripcion_materia_repitiente)
        return render(request, 'editar_inscripcion_materia_repitiente.html', {'form': form, 'inscripcion_materia_repitiente': inscripcion_materia_repitiente})

    def post(self, request, id_inscripcion_repitiente, *args, **kwargs):
        inscripcion_materia_repitiente = get_object_or_404(InscripcionMateriaRepitiente, id_Inscripcion_Repitiente=id_inscripcion_repitiente)
        form = InscripcionMateriaRepitienteForm(request.POST, instance=inscripcion_materia_repitiente)
        if form.is_valid():
            messages.success(request, "Modificado correctamente") 
            form.save()
            return redirect('lista_inscripciones_materias_repitientes')
        return render(request, 'editar_inscripcion_materia_repitiente.html', {'form': form, 'inscripcion_materia_repitiente': inscripcion_materia_repitiente})

class EliminarInscripcionMateriaRepitienteView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def post(self, request, id_inscripcion_repitiente, *args, **kwargs):
        inscripcion_materia_repitiente = get_object_or_404(InscripcionMateriaRepitiente, id_Inscripcion_Repitiente=id_inscripcion_repitiente)
        messages.success(request, "Eliminado correctamente")
        inscripcion_materia_repitiente.delete()
        return redirect('lista_inscripciones_materias_repitientes')

    def get(self, request, id_inscripcion_repitiente, *args, **kwargs):
        inscripcion_materia_repitiente = get_object_or_404(InscripcionMateriaRepitiente, id_Inscripcion_Repitiente=id_inscripcion_repitiente)
        return render(request, 'eliminar_inscripcion_materia_repitiente.html', {'inscripcion_materia_repitiente': inscripcion_materia_repitiente})

class ListaInscripcionesMateriasRepitientesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración
    redirect_field_name = 'ingresar'

    def get(self, request, *args, **kwargs):
        inscripciones_materias_repitientes = InscripcionMateriaRepitiente.objects.all()
        return render(request, 'lista_inscripciones_materias_repitientes.html', {'inscripciones_materias_repitientes': inscripciones_materias_repitientes})

#=======================================================================================================#
#=======================================================================================================#
from django.shortcuts import render
from .models import Estudiante, InscripcionEstudiante, InscripcionMateriaRepitiente, InscripcionMateriaPendiente

class EstadisticasEstudiantesView(LoginRequiredMixin, View):
    login_url = 'login_user'  # Ajusta esto según tu configuración

    def get(self, request, *args, **kwargs):
        # Obtener las estadísticas que necesitas
        total_estudiantes = Estudiante.objects.count()
        total_inscripciones = InscripcionEstudiante.objects.count()
        total_repitiente = InscripcionMateriaRepitiente.objects.count()
        total_pendiente = InscripcionMateriaPendiente.objects.count()
        total_femenino = Estudiante.objects.filter(Genero_Estudiante='Femenino').count()
        total_masculino = Estudiante.objects.filter(Genero_Estudiante='Masculino').count()
        total_Regulares = InscripcionEstudiante.objects.filter(Condicion_Inscripcion='Regular').count()
        total_NoCursante = InscripcionMateriaBachillerNoCursante.objects.count()

        # Puedes continuar agregando más estadísticas según tus necesidades

        # Pasar las estadísticas al template
        context = {
            'total_NoCursante': total_NoCursante,
            'total_Regulares': total_Regulares,
            'total_estudiantes': total_estudiantes,
            'total_inscripciones': total_inscripciones,
            'total_repitiente': total_repitiente,
            'total_pendiente': total_pendiente,
            'total_femenino': total_femenino,
            'total_masculino': total_masculino,
            # Agrega más variables según las estadísticas que quieras mostrar
        }

        # Renderizar el template con las estadísticas
        return render(request, 'estadisticas_estudiantes.html', context)



#=======================================================================================================#
#=======================================================================================================#
#Constancia
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from django.http import HttpResponse
from datetime import date
from django.shortcuts import get_object_or_404


def generar_constancia_estudios(request, cedula_estudiante):
    try:
        # Obtén los datos del alumno
        estudiante = get_object_or_404(Estudiante, Cedula_Estudiante=cedula_estudiante)
        inscripcionestudiante = InscripcionEstudiante.objects.filter(Cedula_Estudiante=estudiante)
        directora = Cargos.objects.get(Cargo_Cargos='Director/a')
        liceo = Institucion.objects.first()

        # Validar si la lista tiene elementos antes de intentar acceder a un índice
        if not inscripcionestudiante:
            raise Http404("No se encontró ninguna inscripción para este estudiante.")
    except Http404:
        # Puedes personalizar la respuesta aquí o redirigir a una página de error específica
        return render(request, '404.html', context={})
    
    # Configura la respuesta HTTP como un archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="constancia_estudios.pdf"'

    # Crea un objeto PDF utilizando reportlab
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Nombre del archivo PDF personalizado para el alumno
    file_name = f"{estudiante.Nombres_Estudiante}_{estudiante.Apellidos_Estudiante}_constancia_estudios.pdf"

    # Define estilos para el contenido del PDF
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Title']

     # Agrega la fecha actual al contenido del PDF
    fecha_actual = date.today().strftime("%d/%m/%Y")


    # Crea un estilo personalizado para texto en negritas
    bold_style = ParagraphStyle(
        name='BoldStyle',
        parent=normal_style,
        fontName='Times-Roman',
        leading=18,
        fontSize=10,
        alignment=1,  # 0=izquierda, 1=centro, 2=derecha, 3=justificar
    )

    # Crea un estilo personalizado para texto en negritas
    boold_style = ParagraphStyle(
        name='BoldStyle',
        parent=normal_style,
        fontName='Times-Roman',
        fontSize=10,
        leading=20,
        alignment=TA_JUSTIFY,
    )

    # Crea un estilo personalizado para texto en negritas
    baold_style = ParagraphStyle(
        name='BoldStyle',
        parent=title_style,
        fontName='Times-Roman',
        fontSize=16,
        textColor=colors.black,
        leading=18,
        alignment=1,  # 0=izquierda, 1=centro, 2=derecha
    )

    # Crea un estilo personalizado para texto en negritas
    bld_style = ParagraphStyle(
        name='BoldStyle',
        parent=normal_style,
        fontName='Times-Roman',
        leading=18,
        fontSize=8,
        alignment=2,  # 0=izquierda, 1=centro, 2=derecha
    )


    # Crea el contenido del PDF
    content = []

    # Agrega una imagen al PDF
    imagen_path = "C:/Users/GetDat/Desktop/Proyecto_Liceo/Liceo/Constancia/imagen/imagen.png"
    imagen = Image(imagen_path, width=500, height=60)
    content.append(imagen)
    content.append(Spacer(1, 12))
    content.append(Paragraph("MINISTERIO DEL PODER POPULAR PARA LA EDUCACIÓN", boold_style))
    content.append(Paragraph(f"LICEO <b>{liceo.Nombre_Institucion}</b>", boold_style))
    content.append(Paragraph("GUANARE-PORTUGUESA", boold_style))
    content.append(Paragraph("<b>OD12711804</b>", boold_style))
    content.append(Spacer(1, 36))
    content.append(Paragraph("<b>CONSTANCIA DE ESTUDIOS</b>", baold_style))
    content.append(Spacer(1, 36))
    content.append(Paragraph(f"Quien suscribe, <b>{directora.Nombres_Cargos} {directora.Apellidos_Cargos}</b>, CI. <b>V-{directora.Cedula_Cargos}</b>, Director(a) del <b>Liceo {liceo.Nombre_Institucion}</b>, certifica que el(a) Estudiante, <b>{estudiante.Nombres_Estudiante} {estudiante.Apellidos_Estudiante}</b>, Cedula de Identidad Nº <b>V-{estudiante.Cedula_Estudiante}</b>, cursa el <b>{inscripcionestudiante[0].Id_Materia_Seccion.Id_Grado.Ano_Grado}</b> año, Sección <b>{inscripcionestudiante[0].Id_Materia_Seccion.Id_Grado.Seccion_Grado}</b>, de <b>Educación Media General</b>, Correspondiente al año Escolar: <b>{inscripcionestudiante[0].Ano_Escolar}</b>", boold_style))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"Constancia que se expide a petición de parte interesada, para los fines legales, en Guanare {fecha_actual}", boold_style))
    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Atentamente:</b>", baold_style))
    content.append(Spacer(1, 12))
    # Centra la información de nombre, cédula y teléfono
    content.append(Paragraph("<u>________________________________</u>", baold_style))
    content.append(Paragraph(f"<b>Nombre y Apellido:</b> {directora.Nombres_Cargos} {directora.Apellidos_Cargos}", bold_style))
    content.append(Paragraph(f"<b>Cédula:</b> {directora.Cedula_Cargos}", bold_style))
    content.append(Paragraph(f"<b>Teléfono:</b> {directora.Telefono_Cargos}", bold_style))
    content.append(Paragraph("<b>Director(A) (E)</b>", bold_style))
    content.append(Spacer(1, 45))
    content.append(Paragraph("<b>Sello</b>", baold_style))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"LICEO <b>{liceo.Nombre_Institucion}</b>", bld_style))
    content.append(Paragraph("GUANARE-PORTUGUESA", bld_style))
    # Agrega el contenido al documento PDF
    doc.build(content)

    # Obtén el contenido generado y envíalo como respuesta HTTP
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

#=======================================================================================================#
#=======================================================================================================#
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Image
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO
from datetime import date
from django.shortcuts import get_object_or_404
from django.http import Http404

def generar_informacion_alumno(request, cedula_estudiante):
    try:
        # Obtén los datos del alumno
        estudiante = get_object_or_404(Estudiante, Cedula_Estudiante=cedula_estudiante)
        inscripcion_estudiante = get_object_or_404(InscripcionEstudiante, Cedula_Estudiante=estudiante)
        representante = get_object_or_404(Representante, estudiante=estudiante)
        liceo = inscripcion_estudiante.id_Institucion
        directora = Cargos.objects.get(Cargo_Cargos='Coordinador de control de estudios y evaluacion')
        regular = InscripcionEstudiante.objects.filter(Condicion_Inscripcion='regular', Cedula_Estudiante=estudiante)
        pendiente = InscripcionMateriaPendiente.objects.filter(id_Inscripcion_Estudiante=inscripcion_estudiante)
        Nocursante = InscripcionMateriaBachillerNoCursante.objects.filter(id_Inscripcion_Estudiante=inscripcion_estudiante)
        repitiente = InscripcionMateriaRepitiente.objects.filter(id_Inscripcion_Estudiante=inscripcion_estudiante)

         
        # Crea un objeto PDF utilizando reportlab
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Define estilos para el contenido del PDF
        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        title_style = styles['Title']

        # Agrega la fecha actual al contenido del PDF
        fecha_actual = date.today().strftime("%d/%m/%Y")

        # Crea un estilo personalizado para texto en negritas
    # Crea un estilo personalizado para texto en negritas
        bold_style = ParagraphStyle(
            name='BoldStyle',
            parent=normal_style,
            fontName='Times-Roman',
            leading=12,
            fontSize=8,
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha, 3=justificar
        )

    # Crea un estilo personalizado para texto en negritas
        boold_style = ParagraphStyle(
            name='BoldStyle',
            parent=normal_style,
            fontName='Times-Roman',
            fontSize=10,
            leading=11,
            alignment=TA_JUSTIFY,
        )

    # Crea un estilo personalizado para texto en negritas
        baold_style = ParagraphStyle(
            name='BoldStyle',
            parent=title_style,
            fontName='Times-Roman',
            fontSize=10,
            textColor=colors.black,
            leading=10,
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha
        )
        baoxld_style = ParagraphStyle(
            name='BoldStyle',
            parent=title_style,
            fontName='Times-Roman',
            fontSize=18,
            textColor=colors.black,
            leading=10,
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha
        )

    # Crea un estilo personalizado para texto en negritas
        bld_style = ParagraphStyle(
            name='BoldStyle',
            parent=normal_style,
            fontName='Times-Roman',
            leading=18,
            fontSize=8,
            alignment=2,  # 1=izquierda, 0=centro, 0=derecha
        )

        # Crea el contenido del PDF
        content = []

        # Agrega una imagen al PDF
        imagen_path = "C:/Users/GetDat/Desktop/Proyecto_Liceo/Liceo/Constancia/imagen/imagen.png"  # Reemplaza con la ruta de tu imagen
        imagen = Image(imagen_path, width=500, height=60)  # Ajusta el ancho y alto según tu imagen
        content.append(imagen)
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"LICEO <b>{liceo.Nombre_Institucion}</b>", boold_style))
        content.append(Paragraph("GUANARE-PORTUGUESA", boold_style))
        content.append(Paragraph("<b>OD12711804</b>", boold_style))
        content.append(Spacer(1, 20))
        content.append(Paragraph("<b>Constancia de inscripcion</b>", baoxld_style))
        content.append(Spacer(1, 20))
        content.append(Paragraph("<b>ESTUDIANTE</b>", baold_style))
        content.append(Paragraph(f"Cédula de Identidad: <b>{estudiante.Cedula_Estudiante}</b>", boold_style))
        content.append(Paragraph(f"Nombre y Apellido: <b>{estudiante.Nombres_Estudiante} {estudiante.Apellidos_Estudiante}</b>", boold_style))
        content.append(Paragraph(f"Fecha de Nacimiento: <b>{estudiante.Fecha_Nacimiento_Estudiante}</b>", boold_style))
        content.append(Paragraph(f"Genero: <b>{estudiante.Genero_Estudiante}</b>", boold_style))
        content.append(Paragraph(f"Lugar de Nacimiento: <b>{estudiante.Lugar_Nacimiento_Estudiante}</b>", boold_style))
        content.append(Paragraph(f"Entidad Federal: <b>{estudiante.Entidad_Federal_Estudiante}</b>", boold_style))
        content.append(Spacer(1, 10))
        content.append(Paragraph("<b>ESCOLARIDAD</b>", baold_style))
        content.append(Paragraph(f"Condicion: <b>{inscripcion_estudiante.Condicion_Inscripcion}</b>", boold_style))
        content.append(Paragraph(f"Año: <b>{inscripcion_estudiante.Id_Materia_Seccion.Id_Grado.Ano_Grado}</b>", boold_style))
        content.append(Paragraph(f"Seccion: <b>{inscripcion_estudiante.Id_Materia_Seccion.Id_Grado.Seccion_Grado}</b>", boold_style))
        content.append(Paragraph(f"Año Escolar: <b>{inscripcion_estudiante.Ano_Escolar}</b>", boold_style))

        # Verifica si se deben generar detalles específicos para el informe
        generar_informe = False

        # Verifica si es estudiante regular
        if regular.exists():
            content.append(Paragraph(f"Materias Regular: <b>{inscripcion_estudiante.Id_Materia_Seccion.get_materias_display_1()}</b>", boold_style))
            generar_informe = True

        # Verifica si es estudiante con materia pendiente
        elif pendiente.exists():
            content.append(Paragraph(f"Materias Regular: <b>{pendiente[0].id_Inscripcion_Estudiante.Id_Materia_Seccion.get_materias_display_1()}</b>", boold_style))
            content.append(Paragraph(f"Materias pendiente: <b>{pendiente[0].get_materias_display_4()}</b>", boold_style))
            generar_informe = True

        # Verifica si es estudiante bachiller no cursante
        elif Nocursante.exists():
            content.append(Paragraph(f"Materias pendiente: <b>{Nocursante[0].get_materias_display_2()}</b>", boold_style))
            generar_informe = True

        # Verifica si es estudiante repitiente
        elif repitiente.exists():
            content.append(Paragraph(f"Materias a repetir: <b>{repitiente[0].get_materias_display_3()}</b>", boold_style))
            generar_informe = True

        # Verifica si se deben generar detalles específicos para el informe
        if generar_informe:
            # Resto del código para crear el informe...

            content.append(Spacer(1, 10))
            content.append(Paragraph("<b>REPRESENTANTE</b>", baold_style))
            content.append(Paragraph(f"Cédula de Identidad: <b>{representante.Cedula_Representante}</b>", boold_style))
            content.append(Paragraph(f"Nombre y Apellido: <b>{representante.Nombres_Representante} {representante.Apellidos_Representante}</b>", boold_style))
            content.append(Paragraph(f"Fecha de Nacimiento: <b>{representante.Fecha_Nacimiento_Representante}</b>", boold_style))
            content.append(Paragraph(f"Genero: <b>{representante.Genero_Representante}</b>", boold_style))
            content.append(Paragraph(f"Lugar de Nacimiento: <b>{representante.Lugar_Nacimiento_Representante}</b>", boold_style))
            content.append(Paragraph(f"Entidad Federal: <b>{representante.Entidad_Federal_Representante}</b>", boold_style))
            content.append(Paragraph(f"Direccion de Habitacion: <b>{representante.Direccion_Habitacion_Representante}</b>", boold_style))
            content.append(Paragraph(f"Telefono: <b>{representante.Telefono1_Representante}</b>", boold_style))
            content.append(Spacer(1, 25))
            content.append(Paragraph("<b>Atentamente:</b>", baold_style))
            content.append(Spacer(1, 10))
    # Centra la información de nombre, cédula y teléfono
            content.append(Paragraph("<u>________________________________</u>", baold_style))
            content.append(Paragraph(f"<b>Nombre y Apellido:</b> {directora.Nombres_Cargos} {directora.Apellidos_Cargos}", bold_style))
            content.append(Paragraph(f"<b>Cédula:</b> {directora.Cedula_Cargos}", bold_style))
            content.append(Paragraph(f"<b>Teléfono:</b> {directora.Telefono_Cargos}", bold_style))
            content.append(Paragraph(" <b>Coordinador de control de estudios y evaluacion</b>", bold_style))
            content.append(Spacer(1, 10))
            content.append(Paragraph("<b>Sello</b>", baold_style))
            content.append(Spacer(1, 25))
            content.append(Paragraph(f"Fecha de Generacion de Datos: {fecha_actual}", bld_style))

            # Agrega el contenido al documento PDF
            doc.build(content)

            # Configura la respuesta HTTP como un archivo PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="informacion_alumno.pdf"'

            # Obtén el contenido generado y envíalo como respuesta HTTP
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)

            return response
        else:
            # No se cumplen las condiciones, no se genera el informe
            return render(request, '404.html', {'mensaje': 'No se generó el informe porque no se cumplen las condiciones'})

    except Http404:
        # Si se produce un error 404, renderiza una plantilla de error personalizada
        return render(request, '404.html', {'mensaje': 'Estudiante no encontrado'})


#=======================================================================================================#
#=======================================================================================================#
# views.py

from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Estudiante
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Image

def generar_informe_estudiantes(request):
    # Obtén todos los estudiantes de la base de datos
    estudiantes = Estudiante.objects.all()

    # Crea un objeto HttpResponse con el tipo de contenido adecuado para el navegador
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_estudiantes.pdf"'

    doc = SimpleDocTemplate(response)

    elements = []

# Encabezado
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Title']

    baold_style = ParagraphStyle(
            name='BoldStyle',
            parent=title_style,
            fontName='Times-Roman',
            fontSize=16,
            textColor=colors.black,
            leading=18,
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha
        )

    logo = "C:/Users/GetDat/Desktop/Proyecto_Liceo/Liceo/Constancia/imagen/imagen.png"
    im = Image(logo, width=500, height=60)
    elements.append(im)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Informe de registros de estudiantes", baold_style ))
    elements.append(Spacer(1, 10))
# Tabla de datos
    table_data = []
    table_data.append(["Cédula", "Nombres", "Apellidos", "Genero"])
    for e in estudiantes:
        table_data.append([e.Cedula_Estudiante, e.Nombres_Estudiante, e.Apellidos_Estudiante, e.Genero_Estudiante])
    
    table = Table(table_data, colWidths=[5*cm, 5*cm, 5*cm])
    table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black), 
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (-1,0), colors.gray)
    ]))
    elements.append(table)

    doc.build(elements)

    return response

#=======================================================================================================#
#=======================================================================================================#

def generar_informe_inscripcion(request):
    # Obtén todos los estudiantes de la base de datos
    Incripc = InscripcionEstudiante.objects.all()

    # Crea un objeto HttpResponse con el tipo de contenido adecuado para el navegador
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_estudiantes.pdf"'

    doc = SimpleDocTemplate(response)

    elements = []

# Encabezado
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Title']

    baold_style = ParagraphStyle(
            name='BoldStyle',
            parent=title_style,
            fontName='Times-Roman',
            fontSize=16,
            textColor=colors.black,
            leading=18,
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha
        )

    logo = "C:/Users/GetDat/Desktop/Proyecto_Liceo/Liceo/Constancia/imagen/imagen.png"
    im = Image(logo, width=500, height=60)
    elements.append(im)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Informe de registros de estudiantes", baold_style ))
    elements.append(Spacer(1, 10))
# Tabla de datos
    table_data = []
    table_data.append(["Estudiante", "Condicion", "Grado", "Año Escolar"])
    for e in Incripc:
        table_data.append([e.Cedula_Estudiante, e.Condicion_Inscripcion, e.Id_Materia_Seccion, e.Ano_Escolar])
    
    table = Table(table_data, colWidths=[5*cm, 5*cm, 5*cm])
    table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black), 
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,0), colors.gray)
    ]))
    elements.append(table)

    doc.build(elements)

    return response