from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Produto,Planos,Contato,Pedido
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import ContatoForm

def app(request):
    return render(request, 'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def produtos(request):

    produtos = Produto.objects.all()
    return render(request,'produtos.html',{"produtos": produtos})

def planos(request):
    planos =  Planos.objects.all()
    return render(request,'planos.html',{"planos":planos})

def contato(request):
    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Sua Mensagem foi enviada com sucesso')
            return redirect(reverse('contato'))
    else:
        form = ContatoForm()
    return render (request,'contato.html',{"form":form})   
  