# forms.py
from django import forms 
from django.forms.widgets import SelectDateWidget
from django_select2.forms import ModelSelect2Widget
from django.core.exceptions import ValidationError
from .models import Representante, Estudiante, InscripcionEstudiante, InscripcionMateriaBachillerNoCursante, InscripcionMateriaRepitiente, InscripcionMateriaPendiente, Materia, MateriaSeccion, Grado, Institucion, Cargos

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    is_superuser = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput)

    class Meta:
        model = CustomUser
        fields = ['Nombres_Completo', 'username', 'email', 'password1', 'password2', 'is_superuser']

#========================================================================================================================#
#========================================================================================================================#

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['Nombres_Completo', 'username', 'email', 'Nombres_Completo', 'is_superuser']

#========================================================================================================================#
#========================================================================================================================#

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

#========================================================================================================================#
#========================================================================================================================#

class RepresentanteForm(forms.ModelForm):
    Cedula_Representante = forms.IntegerField(min_value=4000000, max_value=32000000)
    Nombres_Representante = forms.CharField(min_length=3, max_length=50)
    Apellidos_Representante = forms.CharField(min_length=3, max_length=50)

    class Meta:
        model = Representante
        fields = '__all__'
        widgets = {
            'Fecha_Nacimiento_Representante': SelectDateWidget(
                years=range(2025, 1950, -1),  # Rango desde 2025 hacia abajo hasta 1900
                attrs={'class': 'custom-date-field'}
            ),
        }

#========================================================================================================================#
#========================================================================================================================#

class EstudianteForm(forms.ModelForm):
    Cedula_Estudiante = forms.IntegerField(min_value=24000000, max_value=32000000)
    Nombres_Estudiante = forms.CharField(min_length=3, max_length=50)
    Apellidos_Estudiante = forms.CharField(min_length=3, max_length=50)
    
    class Meta:
        model = Estudiante
        fields = '__all__'
        widgets = {
            'Fecha_Registro_Estudiante': forms.DateInput(attrs={'type': 'date'}),
            'Fecha_Nacimiento_Estudiante': SelectDateWidget(
                years=range(2025, 2004, -1),  # Rango desde 2025 hacia abajo hasta 1900
                attrs={'class': 'custom-date-field'}
            ),
        }
        
#========================================================================================================================#
#========================================================================================================================#

class InscripcionEstudianteForm(forms.ModelForm):
    class Meta:
        model = InscripcionEstudiante
        fields = '__all__'
        widgets = {
            'Fecha_Inscripcion': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones de id_Inscripcion_Estudiante para incluir solo aquellos con condición 'Regular'
        self.fields['id_cargos'].queryset = Cargos.objects.filter(Cargo_Cargos='Coordinador de control de estudios y evaluacion')

#========================================================================================================================#
#========================================================================================================================#

class InscripcionMateriaRepitienteForm(forms.ModelForm):
    class Meta:
        model = InscripcionMateriaRepitiente
        fields = '__all__'

    Materias_pendientes = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_Materias_pendientes(self):
        materias_pendientes = self.cleaned_data['Materias_pendientes']

        # Validación de longitud para el campo Materias_pendientes
        min_length = 3
        max_length = 6

        if len(materias_pendientes) < min_length or len(materias_pendientes) > max_length:
            raise forms.ValidationError(f'Ingrese entre {min_length} y {max_length} materias.')

        return materias_pendientes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones de id_Inscripcion_Estudiante para incluir solo aquellos con condición 'Regular'
        self.fields['id_Inscripcion_Estudiante'].queryset = InscripcionEstudiante.objects.filter(Condicion_Inscripcion='Repetiente')

#========================================================================================================================#
#========================================================================================================================#

class InscripcionMateriaBachillerNoCursanteForm(forms.ModelForm):
    class Meta:
        model = InscripcionMateriaBachillerNoCursante
        fields = ['id_Inscripcion_Estudiante', 'materias_pendientes']

    materias_pendientes = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_Materias_pendientes(self):
        materias_pendientes = self.cleaned_data['Materias_pendientes']

        # Validación de longitud para el campo Materias_pendientes
        min_length = 1
        max_length = 2

        if len(materias_pendientes) < min_length or len(materias_pendientes) > max_length:
            raise forms.ValidationError(f'Ingrese entre {min_length} y {max_length} materias.')

        return materias_pendientes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones de id_Inscripcion_Estudiante para incluir solo aquellos con condición 'Bachiller no cursante'
        self.fields['id_Inscripcion_Estudiante'].queryset = InscripcionEstudiante.objects.filter(Condicion_Inscripcion='Bachiller no cursante')

#========================================================================================================================#
#========================================================================================================================#

class InscripcionMateriaPendienteForm(forms.ModelForm):
    class Meta:
        model = InscripcionMateriaPendiente
        fields = '__all__'

    materias_pendientes = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_Materias_pendientes(self):
        materias_pendientes = self.cleaned_data['Materias_pendientes']

        # Validación de longitud para el campo Materias_pendientes
        min_length = 1
        max_length = 2

        if len(materias_pendientes) < min_length or len(materias_pendientes) > max_length:
            raise forms.ValidationError(f'Ingrese entre {min_length} y {max_length} materias.')

        return materias_pendientes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra las opciones de id_Inscripcion_Estudiante para incluir solo aquellos con condición 'Regular'
        self.fields['id_Inscripcion_Estudiante'].queryset = InscripcionEstudiante.objects.filter(Condicion_Inscripcion='Regular con materia pendiente')

#========================================================================================================================#
#========================================================================================================================#

class MateriaForm(forms.ModelForm):   
    Nombre_Materia = forms.CharField(min_length=3, max_length=50)
    
    class Meta:
        model = Materia
        fields = '__all__'

#========================================================================================================================#
#========================================================================================================================#

class MateriaSeccionForm(forms.ModelForm):
    class Meta:
        model = MateriaSeccion
        fields = ['Id_Materia_Seccion', 'Materias', 'Id_Grado']

    Materias = forms.ModelMultipleChoiceField(
        queryset=Materia.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def clean_materias(self):
        Materias = self.cleaned_data['Materias']

        # Limitar la cantidad de materias seleccionadas
        max_materias = 5
        if len(Materias) > max_materias:
            raise forms.ValidationError(f'Seleccione como máximo {max_materias} materias.')

        return Materias

#========================================================================================================================#
#========================================================================================================================#

class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = '__all__'

#========================================================================================================================#
#========================================================================================================================#

class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = '__all__'

#========================================================================================================================#
#========================================================================================================================#

class CargosForm(forms.ModelForm):

    Cedula_Cargos = forms.IntegerField(min_value=4000000, max_value=32000000)
    Nombres_Cargos = forms.CharField(min_length=3, max_length=50)
    Apellidos_Cargos = forms.CharField(min_length=3, max_length=50)

    class Meta:
        model = Cargos
        fields = '__all__'
        widgets = {
            'Fecha_Ingreso_Cargos': forms.DateInput(attrs={'type': 'date'}),
            'Fecha_Egreso_Cargos': forms.DateInput(attrs={'type': 'date'}),
        }
