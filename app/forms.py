# sua_app/forms.py
from django import forms
from .models import Contato 

class ContatoForm(forms.ModelForm): 
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'mensagem']
        