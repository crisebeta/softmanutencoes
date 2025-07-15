from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('novo/', views.novo_produto, name='novo_produto'),
    path('<int:pk>/', views.detalhe_produto, name='detalhe_produto'),
    path('<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    path('<int:pk>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nova/', views.nova_categoria, name='nova_categoria'),
] 