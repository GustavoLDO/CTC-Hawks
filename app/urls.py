from django.urls import path
from . import views

urlpatterns = [
    path('', views.app, name="app"),
    path('sobre', views.sobre, name="sobre"),
    path('produtos', views.produtos, name="produtos"),
    path('planos', views.planos, name="planos"),
    path('contato',views.contato, name="contato"),

]