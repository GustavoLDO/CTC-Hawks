from django.urls import path
from . import views

urlpatterns = [
    path('', views.app, name="app"),
    path('sobre', views.sobre, name="sobre"),
    path('salvar-usuario', views.salvarUsuario, name="salvarUsuario"),
    path('login', views.loginUsuario, name="loginUsuario"),
    path('logout', views.logoutUsuario, name="logoutUsuario"),
    path('planos', views.planos, name="planos"),
    path('contato',views.contato, name="contato"),

    path('produtos', views.produtos, name="produtos"),
    path('produto/<int:id>/', views.produto_detalhe, name='produto_detalhe'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path('carrinho/adicionar/<int:id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/atualizar/<int:id>/', views.atualizar_quantidade, name='atualizar_quantidade'),
    path('carrinho/adicionar-plano/<int:id>', views.adicionar_plano_carrinho, name='adicionar_plano_carrinho')
]