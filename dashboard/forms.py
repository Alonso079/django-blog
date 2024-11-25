from django import forms
from .models import Autor
from blog.models import Blog  # Cambiar Blog a Publicacion si es necesario

class EditarAutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['imagen_autor', 'nombre', 'apellido', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'imagen_autor': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class CrearPublicacionForm(forms.ModelForm):
    class Meta:
        model = Blog  # Asegúrate de usar el modelo Blog aquí
        fields = ['titulo', 'detalle', 'categoria', 'etiquetas', 'imagen']  # Cambié 'contenido' por 'detalle'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la publicación'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe los detalles aquí...'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'etiquetas': forms.CheckboxSelectMultiple(),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo

    def clean_detalle(self):
        detalle = self.cleaned_data.get('detalle')
        if len(detalle) < 20:
            raise forms.ValidationError("El detalle debe tener al menos 20 caracteres.")
        return detalle