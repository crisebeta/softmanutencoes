from django.urls import path
from . import views

app_name = 'importacoes'

urlpatterns = [
    path('', views.importacoes, name='importacoes'),
    path('clientes/', views.importar_clientes, name='importar_clientes'),
    path('servicos/', views.importar_servicos, name='importar_servicos'),
    path('despesas/', views.importar_despesas, name='importar_despesas'),
    # As URLs específicas serão adicionadas aqui posteriormente
] 