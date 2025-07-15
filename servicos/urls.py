from django.urls import path
from . import views

app_name = 'servicos'

urlpatterns = [
    path('', views.lista_servicos, name='lista_servicos'),
    path('novo/', views.novo_servico, name='novo_servico'),
    path('<int:pk>/', views.detalhe_servico, name='detalhe_servico'),
    path('<int:pk>/editar/', views.editar_servico, name='editar_servico'),
    path('<int:pk>/excluir/', views.excluir_servico, name='excluir_servico'),
    path('excluir/<int:pk>/', views.excluir_servico, name='excluir_servico'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/pdf/', views.gerar_pdf_servico, name='gerar_pdf_servico'),
] 