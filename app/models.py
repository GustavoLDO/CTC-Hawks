from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Pagina(models.Model):
    # O verbose_name não é o dado do site, ele é apenas a "Etiqueta" (Rótulo) do campo que vai aparecer para você lá no Painel Administrativo.

    nome_do_site = models.CharField(max_length=100, verbose_name="Nome do Site")
    logo_do_site = models.ImageField(upload_to='logos/', verbose_name="Logo do Site", validators=[FileExtensionValidator(['pdf', 'svg', 'png', 'jpg', 'jpeg'])])
    texto_chamada = models.TextField(verbose_name="Texto da Chamada (Hero)")
    texto_sobre = models.TextField(verbose_name="Texto Sobre Nós")
    imagem_sobre = models.ImageField(upload_to='sobre/', verbose_name="Imagem da Seção Sobre")

    endereco = models.TextField(verbose_name="Endereço Completo")
    email = models.EmailField(verbose_name="E-mail de Contato")
    whatsapp = models.CharField(max_length=20, verbose_name="Número do WhatsApp")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_do_site

    class Meta:
        verbose_name = "Configuração da Página"
        verbose_name_plural = "Configurações da Página"

class Produto(models.Model):

    #Produto
    nome_produto = models.CharField(max_length=100 , verbose_name= "Nome do Produto")
    estoque_produto = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(0)],verbose_name="Estoque do Produto")
    preco_produto =  models.DecimalField(max_digits=5,decimal_places=2,verbose_name= "Preço do Produto")
    descricao_produto =  models.CharField(max_length=120,verbose_name="Descrição do Produto")
    imagem_produto = models.ImageField(upload_to='produtos/', verbose_name="Imagem dos Produtos ")
    
    criado_em_produto = models.DateTimeField(auto_now_add=True)
    atualizado_em_produto = models.DateTimeField(auto_now=True)          

    def __str__(self):
        return self.nome_produto  
    
class Contato(models.Model):

    #Contato
    nome = models.CharField(max_length= 100, verbose_name=" Nome para Contato")
    email =  models.EmailField(verbose_name="E-mail de Contato",unique=True)
    mensagem = models.CharField(max_length=500,verbose_name="Mesagem para Contato")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Planos(models.Model):

    #Planos
    tipo_plano = models.CharField(max_length= 100, verbose_name="Tipo do Plano")
    descricao_plano = models.CharField(max_length=120,verbose_name="Descrição do Plano")
    preco_plano =  models.DecimalField(max_digits=5,decimal_places=2,verbose_name="Preço do Plano")

    class Meta:
        verbose_name = "Plano"
        verbose_name_plural = "Planos"

    def __str__(self):
        return self.tipo_plano

class Pedido (models.Model):
    # ForeignKey conecta este pedido ao usuário logado (User do Django)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # ForeignKey conecta ao Produto real no banco de dados
    # null=True permite que o pedido seja de um Plano (sem produto)
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True)
   
    # null=True permite que o pedido seja de um Produto (sem plano)
    plano = models.ForeignKey(Planos, on_delete=models.SET_NULL, null=True, blank=True)

    quantidade = models.IntegerField(default=1, validators=[MaxValueValidator(100),MinValueValidator(0)],verbose_name="quantidade de Produto por Pedidos")
    data = models.DateTimeField(auto_now_add=True)

    @property
    def preco_total(self):
        if self.produto:
            return self.quantidade * self.produto.preco_produto
        elif self.plano:
            return self.quantidade * self.plano.preco_plano
        return 0

    # Retorna o nome do item (seja produto ou plano) para o template
    @property
    def nome_item(self):
        if self.produto:
            return self.produto.nome_produto
        elif self.plano:
            return f"Plano: {self.plano.tipo_plano}"
        return "Item desconhecido"

    # Retorna a imagem (se for produto) para o template
    @property
    def imagem_item(self):
        if self.produto and self.produto.imagem_produto:
            return self.produto.imagem_produto.url
        return None

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens dos Pedidos"

    def __str__(self):
        return f"{self.quantidade}x {self.nome_item} ({self.usuario.username})"
