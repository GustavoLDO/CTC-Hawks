from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import Contato 

class ContatoForm(forms.ModelForm): 
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        
