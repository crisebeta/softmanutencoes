from django.urls import path
from . import views

app_name = 'despesas'

urlpatterns = [
    path('', views.lista_despesas, name='lista_despesas'),
    path('nova/', views.nova_despesa, name='nova_despesa'),
    path('editar/<int:pk>/', views.editar_despesa, name='editar_despesa'),
    path('excluir/<int:pk>/', views.excluir_despesa, name='excluir_despesa'),
    path('detalhe/<int:pk>/', views.detalhe_despesa, name='detalhe_despesa'),
] 