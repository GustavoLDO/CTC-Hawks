from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from app.forms import *
from django.urls import reverse
# Create your views here.


def app(request):
    pagina_config = Pagina.objects.first()
    produtos_preview = Produto.objects.all().order_by('-id')[:3]

    if request.method == "POST":
        form = ContatoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Sua mensagem foi enviada com sucesso!')
                return redirect('/#contato') 
            except Exception as e:
                messages.error(request, 'Erro ao enviar mensagem. Verifique se o e-mail já foi usado.')
        else:
            messages.error(request, 'Erro no formulário. Verifique os campos.')

    return render(request, 'home.html', {"pagina":pagina_config, "produtos":produtos_preview})

def sobre(request):
    return render(request, 'sobre.html')

def produtos(request):

    produtos = Produto.objects.all()
    return render(request,'produtos.html',{"produtos": produtos})

def salvarUsuario(request):
    formulario = FormUsuario(request.POST or None)
    if request.POST:
        if formulario.is_valid():
            # Cria mas não salva no banco
            usuario = formulario.save(commit=False)

            # Criptografa a senha
            usuario.set_password(formulario.cleaned_data['password1'])

            usuario.save()
            return redirect('loginUsuario')
    return render(request, "salvarUsuario.html", {'form':formulario})

def loginUsuario(request):
    if request.POST:
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        usuario = authenticate(request, username=nome, password=senha)
        
        if usuario is not None:
            login(request, usuario)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuário ou senha incorretos")
    return render(request,'login.html')

@login_required(login_url='loginUsuario')
def dashboard(request):
    if not request.user:
        return redirect("loginUsuario")
    itens = Pedido.objects.filter(usuario=request.user)
    total = sum(item.preco_total for item in itens)

    return render(request, "dashboard.html", {"usuario":request.user, 'itens':itens, 'total':total})

        
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


# Funções - Dashboard
def produto_detalhe(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produto_detalhe.html', {'produto':produto})

@login_required(login_url='loginUsuario')
def adicionar_carrinho(request, id):
    produto = get_object_or_404(Produto, id=id)

    pedido, created = Pedido.objects.get_or_create(
        usuario=request.user,
        produto=produto,
        defaults={'quantidade':1}
    )

    if not created:
        pedido.quantidade += 1
        pedido.save()
        messages.success(request, f"+1 {produto.nome_produto} adicionado!")
    else:
        messages.success(request, f"{produto.nome_produto} adicionado ao carrinho!")
    
    return redirect('dashboard')

@login_required(login_url='loginUsuario')
def remover_carrinho(request, id):
    pedido = get_object_or_404(Pedido, id=id, usuario=request.user)
    pedido.delete()
    messages.warning(request, "Item removido do carrinho")
    return redirect('dashboard')

@login_required(login_url='loginUsuario')
def atualizar_quantidade(request, id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=id, usuario=request.user)
        try:
            nova_qtd = int(request.POST.get('quantidade', 1))
            estoque = pedido.produto.estoque_produto if pedido.produto else 999
            
            if nova_qtd > 0 and nova_qtd <= estoque:
                pedido.quantidade = nova_qtd
                pedido.save()
            elif nova_qtd > estoque:
                messages.error(request, f"Estoque insuficiente. Apenas {estoque} disponíveis.")
            else:
                pedido.delete()
        except ValueError:
            pass
    return redirect('dashboard')

def logoutUsuario(request):
    logout(request)
    messages.info(request, "Você saiu da conta.")
    return redirect('loginUsuario')

@login_required(login_url='loginUsuario')
def adicionar_plano_carrinho(request, id):
    plano = get_object_or_404(Planos, id=id)
    
    pedido, created = Pedido.objects.get_or_create(
        usuario=request.user,
        plano=plano,
        defaults={'quantidade': 1}
    )
    
    if not created:
        messages.info(request, f"O plano '{plano.tipo_plano}' já está no seu carrinho.")
    else:
        messages.success(request, f"Plano '{plano.tipo_plano}' adicionado ao carrinho com sucesso!")
    
    return redirect('dashboard')
  
