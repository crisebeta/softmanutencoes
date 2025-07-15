from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('novo/', views.novo_cliente, name='novo_cliente'),
    path('<int:pk>/', views.detalhe_cliente, name='detalhe_cliente'),
    path('<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('<int:pk>/excluir/', views.excluir_cliente, name='excluir_cliente'),
] 