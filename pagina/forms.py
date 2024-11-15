from django import forms
from django.contrib.auth.forms import UserCreationForm
from pagina.models import CustomUser
from pagina.models import Categoria

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido. Ingresa una dirección de correo válida.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        
        
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'avatar']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']